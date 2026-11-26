#!/usr/bin/env python3
"""Audit PostgreSQL en lecture seule, sans dépendance Python externe."""
import argparse, subprocess, os, json, html, datetime, pathlib, sys, re
VERSION='1.0.0'
# Chaque contrôle retourne un nombre d'éléments à examiner, sans données sensibles.
CHECKS=[
('SEC01','Superutilisateurs','INFO',"SELECT count(*) FROM pg_roles WHERE rolsuper AND rolcanlogin",'Justifier chaque compte superutilisateur.'),
('SEC02','Comptes avec création de rôles','WARN',"SELECT count(*) FROM pg_roles WHERE rolcreaterole AND rolcanlogin AND NOT rolsuper",'Limiter CREATEROLE aux administrateurs autorisés.'),
('SEC03','Comptes avec création de bases','INFO',"SELECT count(*) FROM pg_roles WHERE rolcreatedb AND rolcanlogin AND NOT rolsuper",'Vérifier le besoin métier de CREATEDB.'),
('SEC04','Contournement RLS','WARN',"SELECT count(*) FROM pg_roles WHERE rolbypassrls AND rolcanlogin AND NOT rolsuper",'Examiner BYPASSRLS.'),
('SEC05','Règles trust','HIGH',"SELECT count(*) FROM pg_hba_file_rules WHERE auth_method='trust'",'Remplacer trust après validation des accès.'),
('SEC06','Erreurs HBA','HIGH',"SELECT count(*) FROM pg_hba_file_rules WHERE error IS NOT NULL",'Corriger les erreurs puis valider le rechargement.'),
('SEC07','Règles réseau sans restriction IPv4/IPv6','WARN',"SELECT count(*) FROM pg_hba_file_rules WHERE address IN ('0.0.0.0','::') AND netmask IN ('0.0.0.0','::') AND auth_method <> 'reject'",'Restreindre les réseaux autorisés.'),
('SEC08','TLS désactivé','WARN',"SELECT (current_setting('ssl')='off')::int",'Activer TLS pour les connexions réseau si nécessaire.'),
('SEC09','Chiffrement des nouveaux mots de passe','WARN',"SELECT (current_setting('password_encryption') <> 'scram-sha-256')::int",'Préférer SCRAM-SHA-256; renouveler les anciens secrets.'),
('SEC10','Règles MD5','WARN',"SELECT count(*) FROM pg_hba_file_rules WHERE auth_method='md5'",'Planifier la migration vers SCRAM; md5 ne prouve pas le format du secret.'),
('SEC11','Règles password','HIGH',"SELECT count(*) FROM pg_hba_file_rules WHERE auth_method='password' AND type <> 'hostssl'",'Éviter password sans transport TLS garanti.'),
('SEC12','Sessions TCP non TLS','INFO',"SELECT count(*) FROM pg_stat_activity a JOIN pg_stat_ssl s USING(pid) WHERE a.client_addr IS NOT NULL AND NOT s.ssl",'Vérifier les exigences de chiffrement et les autres transports sécurisés.'),
('SEC13','Écoute toutes interfaces','WARN',"SELECT ('*'=ANY(string_to_array(current_setting('listen_addresses'),',')))::int",'Limiter les interfaces et contrôler le pare-feu.'),
('SEC14','Journalisation des connexions','INFO',"SELECT (current_setting('log_connections')='off')::int",'Définir une politique de journalisation adaptée à la version.'),
('SEC15','Journalisation des déconnexions','INFO',"SELECT (current_setting('log_disconnections')='off')::int",'Évaluer les besoins de traçabilité.'),
('SEC16','CREATE public accordé à PUBLIC','WARN',"SELECT count(*) FROM pg_namespace n CROSS JOIN LATERAL aclexplode(coalesce(n.nspacl,acldefault('n',n.nspowner))) a WHERE n.nspname='public' AND a.grantee=0 AND a.privilege_type='CREATE'",'Réviser CREATE sur public après analyse des applications.'),
('SEC17','Fonctions SECURITY DEFINER accessibles à PUBLIC','WARN',"SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace CROSS JOIN LATERAL aclexplode(coalesce(p.proacl,acldefault('f',p.proowner))) a WHERE p.prosecdef AND n.nspname NOT IN ('pg_catalog','information_schema') AND a.grantee=0 AND a.privilege_type='EXECUTE'",'Vérifier EXECUTE, propriétaire et search_path.'),
('SEC18','Rôles de lecture de fichiers serveur','HIGH',"SELECT count(*) FROM pg_roles r WHERE r.rolcanlogin AND NOT r.rolsuper AND pg_has_role(r.oid,'pg_read_server_files','MEMBER')",'Limiter les accès aux fichiers serveur.'),
('SEC19','Rôles d’écriture de fichiers serveur','HIGH',"SELECT count(*) FROM pg_roles r WHERE r.rolcanlogin AND NOT r.rolsuper AND pg_has_role(r.oid,'pg_write_server_files','MEMBER')",'Limiter les écritures sur le serveur.'),
('SEC20','Rôles d’exécution de programmes serveur','HIGH',"SELECT count(*) FROM pg_roles r WHERE r.rolcanlogin AND NOT r.rolsuper AND pg_has_role(r.oid,'pg_execute_server_program','MEMBER')",'Réserver cette capacité aux comptes de confiance.'),
('SEC21','Comptes expirés','INFO',"SELECT count(*) FROM pg_roles WHERE rolcanlogin AND rolvaliduntil < now()",'Examiner les comptes expirés; expiration limitée aux mots de passe.'),
('SEC22','Erreurs de configuration','HIGH',"SELECT count(*) FROM pg_file_settings WHERE error IS NOT NULL",'Examiner les erreurs de configuration sans modifier les fichiers.'),
('SEC23','Paramètres en attente de redémarrage','INFO',"SELECT count(*) FROM pg_settings WHERE pending_restart",'Planifier les redémarrages nécessaires.'),
('SEC24','Secrets MD5 existants','WARN',"SELECT count(*) FROM pg_authid WHERE rolpassword LIKE 'md5%'",'Renouveler les secrets MD5; aucun secret exporté.'),
]
def query(args, sql):
    env={k:v for k,v in os.environ.items() if k not in ('PGOPTIONS','PGSERVICE','PGSERVICEFILE')}
    env.update(PGOPTIONS='-c default_transaction_read_only=on -c statement_timeout=10000 -c lock_timeout=2000',PGCONNECT_TIMEOUT='5')
    cmd=['psql','-X','-w','-A','-t','-q','-v','ON_ERROR_STOP=1','-h',args.host,'-p',str(args.port),'-d',args.database]
    if args.user: cmd+=['-U',args.user]
    r=subprocess.run(cmd,input=sql+';\n',text=True,capture_output=True,env=env,timeout=20)
    if r.returncode: raise RuntimeError('Requête inaccessible ou non compatible (code '+str(r.returncode)+')')
    return r.stdout.strip()
def collect(args):
    version=query(args,'SHOW server_version_num')
    if not version.isdigit(): raise RuntimeError('Version serveur invalide')
    results=[]
    for ident,title,severity,sql,advice in CHECKS:
        try:
            n=int(query(args,sql)); status='OK' if n==0 else ('INFO' if severity=='INFO' else 'REVIEW')
        except (RuntimeError,ValueError,subprocess.TimeoutExpired): n=None; status='UNKNOWN'
        results.append(dict(id=ident,title=title,severity=severity,status=status,count=n,recommendation=advice))
    return dict(version=VERSION,server_version_num=int(version),database=args.database,port=args.port,generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=results)
def render(report):
    e=lambda x:html.escape(str(x))
    rows=''.join('<tr>'+''.join('<td>'+e(c[k])+'</td>' for k in ('id','title','severity','status','count','recommendation'))+'</tr>' for c in report['checks'])
    return '<!doctype html><html lang="fr"><meta charset="utf-8"><title>Audit PostgreSQL</title><style>body{font:16px system-ui;margin:3%;color:#17324d}table{border-collapse:collapse;width:100%}td,th{padding:10px;border:1px solid #ccd6df;text-align:left}th{background:#17324d;color:white}tr:nth-child(even){background:#eef4f8}</style><h1>PostgreSQL Security Auditor</h1><p>'+e(report['generated_at'])+' — Base : '+e(report['database'])+'</p><p>REVIEW : examen requis. UNKNOWN : contrôle non conclu. INFO : inventaire. OK : aucun élément détecté par ce contrôle.</p><table><thead><tr><th>ID</th><th>Contrôle</th><th>Priorité</th><th>État</th><th>Nombre</th><th>Recommandation</th></tr></thead><tbody>'+rows+'</tbody></table><p>Audit indicatif, non exhaustif. Aucun score de conformité.</p></html>'
def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--version',action='version',version=VERSION); p.add_argument('--host',default='/var/run/postgresql'); p.add_argument('--port',type=int,default=5432); p.add_argument('--database',default='postgres'); p.add_argument('--user'); p.add_argument('--output',default='reports'); p.add_argument('--interactive',action='store_true'); a=p.parse_args()
    if a.interactive:
        if pathlib.Path('/etc/os-release').exists(): print(pathlib.Path('/etc/os-release').read_text())
        try: subprocess.run(['pg_lsclusters'],check=False)
        except FileNotFoundError: pass
        a.port=int(input('Port PostgreSQL [5432] : ') or '5432'); a.database=input('Base [postgres] : ') or 'postgres'; a.output=input('Dossier de rapports [reports] : ') or 'reports'
    if not 1<=a.port<=65535 or not re.fullmatch(r'[A-Za-z0-9_.-]+',a.database): p.error('Port ou nom de base invalide')
    os.umask(0o077)
    try:
        report=collect(a); folder=pathlib.Path(a.output); folder.mkdir(mode=0o700,parents=True,exist_ok=True)
        if folder.is_symlink() or folder.stat().st_uid!=os.getuid() or folder.stat().st_mode & 0o077: raise RuntimeError('Dossier de rapports non privé ou non détenu par le compte courant')
        stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        for ext,content in [('json',json.dumps(report,ensure_ascii=False,indent=2)),('html',render(report))]:
            with (folder/f'audit-{stamp}.{ext}').open('x',encoding='utf-8') as f: f.write(content)
        print('Rapports :',folder,stamp); return 2 if any(c['status']=='UNKNOWN' for c in report['checks']) else 0
    except (RuntimeError,OSError,subprocess.TimeoutExpired) as ex: print('Échec :',ex,file=sys.stderr); return 1
if __name__=='__main__': sys.exit(main())
