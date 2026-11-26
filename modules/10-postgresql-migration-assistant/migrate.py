#!/usr/bin/env python3
"""Assistant de migration logique, sans suppression automatique."""
import argparse, csv, hashlib, html, json, os, re, subprocess, sys
from pathlib import Path


def run(args, **kw):
    return subprocess.run(args, check=True, text=True, **kw)


def endpoint(service, db):
    # Les services libpq évitent les mots de passe dans les arguments.
    for v in (service, db):
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]{0,62}', v):
            raise ValueError('Identifiant simple requis: '+v)
    return f'service={service} dbname={db} connect_timeout=5'


def sql(conn, query):
    env = dict(os.environ, PGOPTIONS='-c default_transaction_read_only=on -c statement_timeout=60000 -c lock_timeout=2000 -c search_path=pg_catalog')
    out = run(['psql','-X','-w','-At','-v','ON_ERROR_STOP=1','-d',conn,'-c',query], env=env, capture_output=True, timeout=75).stdout
    return json.loads(out)


QUERIES = {
 'serveur': "SELECT json_build_object('version',current_setting('server_version_num')::int,'database',current_database(),'encoding',getdatabaseencoding(),'collation',datcollate,'ctype',datctype,'recovery',pg_is_in_recovery()) FROM pg_database WHERE datname=current_database()",
 'bases': "SELECT coalesce(json_agg(datname ORDER BY datname),'[]') FROM pg_database WHERE datallowconn",
 'roles': "SELECT coalesce(json_agg(r ORDER BY rolname),'[]') FROM (SELECT rolname,rolsuper,rolcanlogin,rolcreaterole,rolcreatedb,rolbypassrls FROM pg_roles) r",
 'appartenances': "SELECT coalesce(json_agg(r ORDER BY role,membre),'[]') FROM (SELECT pg_get_userbyid(roleid) role,pg_get_userbyid(member) membre,admin_option FROM pg_auth_members) r",
 'extensions': "SELECT coalesce(json_agg(r ORDER BY extname),'[]') FROM (SELECT extname,extversion FROM pg_extension) r",
 'extensions_disponibles': "SELECT coalesce(json_agg(r ORDER BY name,version),'[]') FROM (SELECT name,version FROM pg_available_extension_versions) r",
 'objets': "SELECT coalesce(json_agg(r ORDER BY schema,nom,type),'[]') FROM (SELECT n.nspname schema,c.relname nom,c.relkind type,pg_get_userbyid(c.relowner) proprietaire,c.relacl::text acl FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname NOT IN ('pg_catalog','information_schema') AND n.nspname NOT LIKE 'pg_toast%' AND n.nspname NOT LIKE 'pg_temp_%') r",
 'schemas': "SELECT coalesce(json_agg(r ORDER BY nspname),'[]') FROM (SELECT nspname,pg_get_userbyid(nspowner) proprietaire,nspacl::text acl FROM pg_namespace WHERE left(nspname,3)<>'pg_' AND nspname<>'information_schema') r",
 'routines': "SELECT coalesce(json_agg(r ORDER BY schema,nom,args),'[]') FROM (SELECT n.nspname schema,p.proname nom,pg_get_function_identity_arguments(p.oid) args,pg_get_userbyid(p.proowner) proprietaire,p.proacl::text acl FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE left(n.nspname,3)<>'pg_' AND n.nspname<>'information_schema') r",
 'tables': "SELECT coalesce(json_agg(r ORDER BY schema,nom),'[]') FROM (SELECT n.nspname schema,c.relname nom,format('%I.%I',n.nspname,c.relname) ident FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE c.relkind='r' AND left(n.nspname,3)<>'pg_' AND n.nspname<>'information_schema') r"
}


def inventory(conn):
    return {k:sql(conn,q) for k,q in QUERIES.items()}


def counts(conn, inv):
    return {t['ident']:sql(conn,'SELECT count(*) FROM ONLY '+t['ident']) for t in inv['tables']}


def assess(src,dst):
    s,t=src['serveur'],dst['serveur']; a,b=s['version']//10000,t['version']//10000
    blockers=[]; warnings=[]
    if not (14<=a<=b<=18): blockers.append('Versions hors périmètre ou rétrogradation.')
    if t['recovery']: blockers.append('Destination en récupération.')
    available={(x['name'],x['version']) for x in dst['extensions_disponibles']}
    for x in src['extensions']:
        if (x['extname'],x['extversion']) not in available: blockers.append('Extension/version absente: '+x['extname']+' '+x['extversion'])
    for k in ('encoding','collation','ctype'):
        if s[k]!=t[k]: warnings.append('Différence '+k+' (base de maintenance cible, pas la future base).')
    missing=sorted({r['rolname'] for r in src['roles']}-{r['rolname'] for r in dst['roles']})
    if missing: warnings.append('Rôles absents: '+', '.join(missing))
    warnings.append('Propriétaires et ACL non restaurés; reconstruire et tester les droits avant bascule.')
    return {'blocages':blockers,'avertissements':warnings}


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''): h.update(chunk)
    return h.hexdigest()


def report(folder,data):
    folder.mkdir(mode=0o700,parents=False,exist_ok=False)
    (folder/'rapport.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
    sections=''.join('<section><h2>'+html.escape(k)+'</h2><pre>'+html.escape(json.dumps(v,ensure_ascii=False,indent=2))+'</pre></section>' for k,v in data.items())
    (folder/'rapport.html').write_text('<!doctype html><html lang="fr"><meta charset="utf-8"><title>Migration PostgreSQL</title><style>body{font:16px system-ui;background:#edf2f6;color:#17354d;max-width:1100px;margin:40px auto;padding:20px}header{background:#17354d;color:white;padding:24px}section{background:white;padding:20px;margin:16px 0;border-radius:8px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}</style><header><h1>Migration Assistant — Rapport technique</h1><p>Inventaire et validation • PostgreSQL</p></header>'+sections+'</html>')


def main():
    os.umask(0o077)
    p=argparse.ArgumentParser(description='Migration logique PostgreSQL 14–18')
    p.add_argument('action',choices=['assess','migrate','verify','interactive']); p.add_argument('--source',default='source'); p.add_argument('--target',default='target'); p.add_argument('--database'); p.add_argument('--destination'); p.add_argument('--output',default='migration-report'); p.add_argument('--apply',action='store_true'); p.add_argument('--source-frozen',action='store_true',help='Confirmer la suspension des écritures source')
    a=p.parse_args()
    if a.action=='interactive':
        a.action=input('Action (assess/migrate/verify): '); a.source=input('Service source: '); a.target=input('Service cible: '); a.database=input('Base source: '); a.destination=input('Nouvelle base cible: '); a.output=input('Nouveau dossier rapport: ')
        if a.action=='migrate': a.source_frozen=input('Écritures suspendues? OUI: ')=='OUI'; a.apply=input('Exécuter? OUI: ')=='OUI'
    if a.action not in ('assess','migrate','verify'): p.error('Action invalide')
    src=endpoint(a.source,a.database or ''); maintenance=endpoint(a.target,'postgres'); dst=endpoint(a.target,a.destination or '')
    if a.source==a.target and a.database==a.destination: p.error('Source et destination identiques')
    folder=Path(a.output).absolute(); s=inventory(src); t=inventory(maintenance if a.action!='verify' else dst); result={'source':s,'cible':t,'evaluation':assess(s,t)}
    if a.action=='assess' or (a.action=='migrate' and not a.apply):
        result['plan']=['Suspendre les écritures','Exporter en format custom','Créer une base cible neuve','Restaurer sans propriétaires ni ACL','Comparer les comptages','Valider droits et application']; report(folder,result); return 2 if result['evaluation']['blocages'] else 0
    if a.action=='verify':
        result['comptages_source']=counts(src,s); result['comptages_cible']=counts(dst,t); result['comptages_identiques']=result['comptages_source']==result['comptages_cible']; report(folder,result); return 0 if result['comptages_identiques'] else 2
    if not a.source_frozen: p.error('Suspendre les écritures et confirmer --source-frozen')
    if result['evaluation']['blocages']: report(folder,result); return 2
    if a.destination in t['bases']: p.error('Base cible existante: refus')
    major=t['serveur']['version']//10000
    for tool in ('pg_dump','pg_restore'):
        v=run([tool,'--version'],capture_output=True).stdout
        if not re.search(r'\b'+str(major)+r'\.',v): p.error('Utiliser les clients de la version cible: '+tool)
    result['comptages_source']=counts(src,s); report(folder,result)
    archive=folder/'source.dump'; run(['pg_dump','-w','-Fc','--no-owner','--no-acl','-d',src,'-f',str(archive)])
    checksum=digest(archive); (folder/'source.dump.sha256').write_text(checksum+'  source.dump\n'); run(['pg_restore','--list',str(archive)],stdout=subprocess.DEVNULL)
    if digest(archive)!=checksum: raise ValueError('Archive altérée')
    run(['createdb','-w','--maintenance-db='+maintenance,'--template=template0','--encoding='+s['serveur']['encoding'],'--lc-collate='+s['serveur']['collation'],'--lc-ctype='+s['serveur']['ctype'],a.destination])
    run(['pg_restore','-w','--exit-on-error','--single-transaction','--no-owner','--no-acl','--no-tablespaces','-d',dst,str(archive)])
    after=inventory(dst); result['cible_apres']=after; result['comptages_cible']=counts(dst,after); result['comptages_identiques']=result['comptages_source']==result['comptages_cible']; report(folder/'validation',result)
    return 0 if result['comptages_identiques'] else 2

if __name__=='__main__':
    try: sys.exit(main())
    except (ValueError,OSError,subprocess.SubprocessError) as e:
        print('Échec: '+str(e)+' — conserver les preuves; aucune suppression automatique.',file=sys.stderr); sys.exit(1)
