#!/usr/bin/env python3
"""Assistant de déploiement PostgreSQL pour Debian et Ubuntu."""
import argparse, os, re, subprocess, shlex, shutil, pathlib, tempfile, datetime, sys
P=pathlib.Path

def run(cmd, apply=False):
    print('+',shlex.join(map(str,cmd)),flush=True)
    if apply: subprocess.run(list(map(str,cmd)),check=True)

def capture(cmd):
    return subprocess.check_output(cmd,text=True,timeout=20)

def platform():
    d={k:v.strip('"') for k,v in (x.split('=',1) for x in P('/etc/os-release').read_text().splitlines() if '=' in x)}
    return d.get('ID',''),d.get('VERSION_ID','')

def memory():
    return int(re.search(r'MemTotal:\s+(\d+)',P('/proc/meminfo').read_text())[1])//1024

def tuning(m):
    # Profil prudent pour serveur dédié; work_mem est par opération.
    return {'shared_buffers':f'{max(16,min(m//4,8192))}MB','effective_cache_size':f'{max(32,m//2)}MB','work_mem':'4MB','maintenance_work_mem':f'{max(32,min(m//16,512))}MB','password_encryption':'scram-sha-256','listen_addresses':'localhost'}

def valid(v,c):
    if v not in range(14,19) or not re.fullmatch(r'[a-zA-Z0-9_]{1,40}',c): raise ValueError('Version ou nom de cluster invalide')

def cluster(v,c):
    valid(v,c)
    for line in capture(['pg_lsclusters','--no-header']).splitlines():
        fields=line.split()
        if fields[:2]==[str(v),c]: return fields
    raise ValueError('Cluster introuvable')

def atomic(path,data):
    fd,tmp=tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as f: f.write(data); f.flush(); os.fsync(f.fileno())
        if path.exists():
            st=path.stat(); os.chown(tmp,st.st_uid,st.st_gid); os.chmod(tmp,st.st_mode & 0o777)
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def configure(a):
    fields=cluster(a.version,a.cluster)
    if fields[3]!='online': raise ValueError('Cluster doit être en ligne pour validation')
    base=P(f'/etc/postgresql/{a.version}/{a.cluster}')
    conf=base/'postgresql.conf'; hba=base/'pg_hba.conf'
    for p in (conf,hba):
        if p.is_symlink() or not p.is_file(): raise ValueError('Configuration non standard')
    settings=tuning(a.ram or memory()); print(settings)
    print('HBA proposé: peer local, SCRAM TCP loopback uniquement. Remplace les règles existantes; réservé au laboratoire neuf.')
    if not a.apply: return
    if not a.fresh_lab: raise ValueError('--fresh-lab obligatoire; ne pas utiliser sur production existante')
    backup=P('/var/backups/pg-deployment-wizard')/f'{a.version}-{a.cluster}'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    os.umask(0o077); backup.mkdir(parents=True,mode=0o700)
    for p in (conf,hba): shutil.copy2(p,backup/p.name)
    print('Sauvegarde:',backup,flush=True)
    try:
        for k,v in settings.items(): run(['pg_conftool',str(a.version),a.cluster,'set',k,v],True)
        atomic(hba,b'local all postgres peer\nlocal all all peer\nhost all all 127.0.0.1/32 scram-sha-256\nhost all all ::1/128 scram-sha-256\n')
        sql=['runuser','-u','postgres','--','psql','-X','-w','-h','/var/run/postgresql','-p',fields[2],'-d','postgres','-v','ON_ERROR_STOP=1','-Atc']
        errors=capture(sql+['SELECT (SELECT count(*) FROM pg_file_settings WHERE error IS NOT NULL)+(SELECT count(*) FROM pg_hba_file_rules WHERE error IS NOT NULL)']).strip()
        if errors!='0': raise RuntimeError('Configuration invalide')
        run(['pg_ctlcluster',str(a.version),a.cluster,'restart'],True)
        capture(sql+['SELECT 1'])
        actual=capture(sql+["SELECT current_setting('listen_addresses') || '|' || current_setting('password_encryption')"]).strip()
        if actual!='localhost|scram-sha-256': raise RuntimeError('Paramètres surchargés')
    except BaseException:
        for p in (conf,hba): atomic(p,(backup/p.name).read_bytes())
        run(['pg_ctlcluster',str(a.version),a.cluster,'restart'],True)
        raise

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('action',choices=['detect','install','create','status','start','stop','restart','configure','rollback','interactive']); p.add_argument('--version',type=int,default=18); p.add_argument('--cluster',default='formation'); p.add_argument('--port',type=int,default=5435); p.add_argument('--ram',type=int); p.add_argument('--backup'); p.add_argument('--apply',action='store_true'); p.add_argument('--fresh-lab',action='store_true'); a=p.parse_args()
    if a.action=='interactive':
        print('Actions: detect, install, create, status, start, stop, restart, configure, rollback')
        args=shlex.split(input('Action et options (sans --apply pour simulation): ')); sys.argv=[sys.argv[0]]+args; return main()
    valid(a.version,a.cluster)
    if not 1024<=a.port<=65535 or (a.ram is not None and not 256<=a.ram<=1048576): p.error('Port ou RAM invalide')
    osid,ver=platform(); print(f'Système: {osid} {ver}; RAM hôte: {memory()} Mio')
    if osid not in ('ubuntu','debian'): raise ValueError('Distribution non prise en charge')
    if a.apply and os.geteuid()!=0: raise ValueError('Exécution réelle: sudo requis')
    if a.apply and a.action not in ('detect','status') and input('Confirmer la modification (OUI): ')!='OUI': return
    if a.action=='detect':
        if shutil.which('pg_lsclusters'): run(['pg_lsclusters'],True)
    elif a.action=='install':
        pkg=f'postgresql-{a.version}'; print(capture(['apt-cache','policy',pkg])); run(['apt-get','install',pkg,'postgresql-common'],a.apply)
    elif a.action=='create': run(['pg_createcluster',str(a.version),a.cluster,'--port',str(a.port),'--start','--auth-local=peer','--auth-host=scram-sha-256'],a.apply)
    elif a.action in ('status','start','stop','restart'): cluster(a.version,a.cluster); run(['pg_ctlcluster',str(a.version),a.cluster,a.action],a.apply or a.action=='status')
    elif a.action=='configure': configure(a)
    elif a.action=='rollback':
        cluster(a.version,a.cluster); base=P(f'/etc/postgresql/{a.version}/{a.cluster}'); root=P(f'/var/backups/pg-deployment-wizard/{a.version}-{a.cluster}'); src=P(a.backup or '/nonexistent').resolve()
        if src.parent!=root.resolve() or not all((src/n).is_file() and not (src/n).is_symlink() for n in ('postgresql.conf','pg_hba.conf')): raise ValueError('Sauvegarde invalide')
        print('Restaurer:',src)
        if a.apply:
            for n in ('postgresql.conf','pg_hba.conf'): atomic(base/n,(src/n).read_bytes())
            run(['pg_ctlcluster',str(a.version),a.cluster,'restart'],True)

if __name__=='__main__':
    try: main()
    except (ValueError,OSError,RuntimeError,subprocess.SubprocessError) as e: print('Erreur:',e,file=sys.stderr); sys.exit(1)
