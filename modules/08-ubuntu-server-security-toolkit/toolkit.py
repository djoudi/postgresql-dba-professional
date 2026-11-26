#!/usr/bin/env python3
"""Administration prudente d'un serveur Ubuntu. Aucun changement sans --apply."""
import argparse, subprocess, os, sys, pathlib, json, html, tempfile, stat, re, pwd, shutil, time
P=pathlib.Path
ROOT=P('/var/backups/ubuntu-security-toolkit')
CONF=P('/etc/ssh/sshd_config.d/00-toolkit-hardening.conf')
def run(*args, check=True):
    return subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=check, timeout=120)
def action(args, apply):
    print('Commande:',repr(args))
    if apply:
        r=run(*args); print(r.stdout)
def require_root():
    if os.geteuid()!=0: raise ValueError('Exécuter avec sudo.')
def profile():
    return 'PubkeyAuthentication yes\nPermitRootLogin no\nPermitEmptyPasswords no\nMaxAuthTries 4\nX11Forwarding no\n'
def audit(output):
    checks=[('Système',['cat','/etc/os-release']),('Noyau',['uname','-r']),('SSH',['sshd','-T']),('Sockets',['ss','-lnt']),('UFW',['ufw','status','verbose']),('Fail2Ban',['fail2ban-client','status']),('Mises à jour',['apt','list','--upgradable']),('Comptes',['getent','passwd']),('Administrateurs',['getent','group','sudo']),('Services',['systemctl','--failed','--no-pager']),('Disque',['df','-h']),('Mémoire',['free','-m'])]
    rows=[]
    for name,cmd in checks:
        try:
            r=run(*cmd,check=False); rows.append(dict(controle=name,statut='COLLECTE' if r.returncode==0 else 'INCONNU',resultat=r.stdout[:50000]))
        except (OSError,subprocess.TimeoutExpired): rows.append(dict(controle=name,statut='INCONNU',resultat='Commande indisponible ou délai dépassé'))
    os.umask(0o077); out=P(output); out.mkdir(mode=0o700,parents=True,exist_ok=True)
    if out.is_symlink() or out.stat().st_uid!=os.getuid() or out.stat().st_mode & 0o077: raise ValueError('Répertoire privé requis (0700).')
    d=P(tempfile.mkdtemp(prefix='audit-',dir=out)); (d/'rapport.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
    cards=''.join('<section><h2>'+html.escape(r['controle'])+' — '+r['statut']+'</h2><pre>'+html.escape(r['resultat'])+'</pre></section>' for r in rows)
    (d/'rapport.html').write_text('<!doctype html><html lang="fr"><meta charset="utf-8"><title>Audit Ubuntu</title><style>body{font:16px system-ui;background:#eef3f7;color:#17354d;max-width:1100px;margin:40px auto;padding:20px}section{background:white;padding:20px;margin:15px 0;border-radius:10px}pre{white-space:pre-wrap;overflow-wrap:anywhere}h1{border-bottom:4px solid #168b88}</style><h1>Ubuntu Security Toolkit — Rapport technique</h1><p>Collecte brute, pas une certification de sécurité. Données sensibles.</p>'+cards+'</html>'); print(d)
def reload_ssh():
    run('sshd','-t'); run('systemctl','reload','ssh.service')
def rollback(folder):
    require_root(); folder=P(folder).resolve(); root=ROOT.resolve()
    if folder.parent!=root or not folder.name.startswith('ssh-'): raise ValueError('Sauvegarde non autorisée')
    if (folder/'present').exists(): shutil.copy2(folder/'original.conf',CONF)
    else: CONF.unlink(missing_ok=True)
    reload_ssh()
def harden(apply):
    print(profile()); print('Conserve le port, les mots de passe et les règles HBA/pare-feu existants.')
    if not apply:return
    require_root(); run('sshd','-t'); run('systemctl','is-active','ssh.service'); ROOT.mkdir(mode=0o700,parents=True,exist_ok=True)
    if ROOT.is_symlink() or ROOT.stat().st_uid != 0 or ROOT.stat().st_mode & 0o077: raise ValueError('Répertoire de sauvegarde non sécurisé')
    if CONF.is_symlink(): raise ValueError('Lien symbolique refusé')
    pending=run('systemctl','list-units','--type=timer','--state=active','--no-legend','ubuntu-toolkit-*.timer').stdout.strip()
    if pending: raise ValueError('Retour SSH déjà programmé : terminer la validation précédente')
    folder=P(tempfile.mkdtemp(prefix='ssh-',dir=ROOT)); unit='ubuntu-toolkit-'+folder.name
    if CONF.exists(): shutil.copy2(CONF,folder/'original.conf'); (folder/'present').touch()
    # Copie autonome pour que le retour arrière survive au déplacement du dépôt.
    shutil.copy2(__file__,folder/'rollback.py')
    run('systemd-run','--unit='+unit,'--on-active=5min','/usr/bin/python3',str(folder/'rollback.py'),'rollback','--backup',str(folder),'--apply')
    try:
        fd,tmp=tempfile.mkstemp(dir=CONF.parent,prefix='.toolkit-'); os.write(fd,profile().encode()); os.close(fd); os.chmod(tmp,0o644); os.replace(tmp,CONF); reload_ssh()
        effective=run('sshd','-T').stdout; print(effective)
    except Exception:
        rollback(folder); raise
    print('Retour automatique dans 5 minutes. Tester une NOUVELLE connexion SSH avant de confirmer.')
    print('Après validation seulement: sudo systemctl stop '+unit+'.timer'); print('Sauvegarde:',folder)
def key_add(user,keyfile,apply):
    account=pwd.getpwnam(user); key=P(keyfile).read_text().strip()
    if '\n' in key or not re.match(r'^(ssh-ed25519|ssh-rsa|ecdsa-sha2-nistp(?:256|384|521)) [A-Za-z0-9+/=]+(?: .*)?$',key): raise ValueError('Clé publique simple requise')
    run('ssh-keygen','-lf',keyfile); print('Ajout de clé pour',user)
    if not apply:return
    require_root()
    # Exécuter les écritures avec les droits du compte cible, jamais root.
    pid=os.fork()
    if pid==0:
        try:
            os.initgroups(user,account.pw_gid); os.setgid(account.pw_gid); os.setuid(account.pw_uid); os.umask(0o077)
            d=P(account.pw_dir)/'.ssh'; d.mkdir(mode=0o700,exist_ok=True)
            if d.is_symlink(): raise ValueError('Lien refusé')
            d.chmod(0o700); f=d/'authorized_keys'; fd=os.open(f,os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
            with os.fdopen(fd,'r+') as stream:
                import fcntl
                fcntl.flock(stream,fcntl.LOCK_EX); os.fchmod(stream.fileno(),0o600); old=stream.read()
                if key not in old.splitlines(): stream.write(('\n' if old and not old.endswith('\n') else '')+key+'\n')
            os._exit(0)
        except Exception as e: print(str(e),file=sys.stderr,flush=True); os._exit(1)
    if os.waitpid(pid,0)[1]: raise ValueError('Échec ajout de clé')
def main():
    p=argparse.ArgumentParser(description='Ubuntu Server Security Toolkit'); p.add_argument('command',choices=['audit','ssh','rollback','key-add','ufw-allow','fail2ban','updates','interactive','detect']); p.add_argument('--apply',action='store_true'); p.add_argument('--output',default=str(P.home()/'security-reports')); p.add_argument('--backup'); p.add_argument('--user'); p.add_argument('--key'); p.add_argument('--source'); p.add_argument('--port',type=int,default=22); a=p.parse_args()
    if a.command=='interactive':
        print('1 Audit | 2 Profil SSH (simulation) | 3 Détection | 0 Quitter'); c=input('Choix : '); a.command={'1':'audit','2':'ssh','3':'detect','0':'exit'}.get(c,'exit'); a.apply=False
    if a.apply: require_root()
    if a.command=='audit': audit(a.output)
    elif a.command=='detect': print(P('/etc/os-release').read_text()); print(run('systemctl','is-active','ssh.socket',check=False).stdout)
    elif a.command=='ssh': harden(a.apply)
    elif a.command=='rollback':
        if not a.backup: p.error('--backup requis')
        if a.apply: rollback(a.backup)
        else: print('Restauration prévue:',a.backup)
    elif a.command=='key-add':
        if not a.user or not a.key: p.error('--user et --key requis')
        key_add(a.user,a.key,a.apply)
    elif a.command=='ufw-allow':
        import ipaddress
        if not a.source or not 1<=a.port<=65535: p.error('Source CIDR et port valides requis')
        source=str(ipaddress.ip_network(a.source,strict=False)); action(['ufw','allow','from',source,'to','any','port',str(a.port),'proto','tcp'],a.apply)
    elif a.command=='fail2ban': action(['apt-get','install','fail2ban'],a.apply)
    elif a.command=='updates': action(['apt-get','install','unattended-upgrades'],a.apply)
if __name__=='__main__':
    try: main()
    except (ValueError,OSError,subprocess.SubprocessError) as e: print('Erreur:',e,file=sys.stderr); sys.exit(1)
