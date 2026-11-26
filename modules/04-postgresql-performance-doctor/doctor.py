#!/usr/bin/env python3
"""Diagnostic PostgreSQL en lecture seule, sans dépendance Python externe."""
import argparse, datetime, html, json, os, pathlib, subprocess, tempfile, shutil

# Les requêtes ne collectent ni texte SQL ni données applicatives.
CHECKS = [
('PER01','Connexions',"SELECT count(*) AS total, count(*) FILTER (WHERE state='active') AS actives, current_setting('max_connections')::int AS maximum FROM pg_stat_activity",'Comparer les connexions aux limites; envisager un pool.'),
('PER02','Transactions longues',"SELECT pid, extract(epoch FROM now()-xact_start)::bigint AS secondes, state FROM pg_stat_activity WHERE pid<>pg_backend_pid() AND xact_start < now()-interval '5 minutes' ORDER BY xact_start LIMIT 100",'Examiner les transactions de plus de cinq minutes.'),
('PER03','Blocages',"SELECT pid, pg_blocking_pids(pid) AS bloqueurs, wait_event FROM pg_stat_activity WHERE cardinality(pg_blocking_pids(pid))>0 LIMIT 100",'Identifier le bloqueur avant toute intervention.'),
('PER04','Attentes',"SELECT wait_event_type, wait_event, count(*) AS sessions FROM pg_stat_activity WHERE state='active' GROUP BY 1,2 ORDER BY 3 DESC",'Les attentes constituent un instantané, pas une mesure historique.'),
('PER05','Cache par base',"SELECT datname, blks_read, blks_hit, round(100.0*blks_hit/nullif(blks_hit+blks_read,0),2) AS hit_pct FROM pg_stat_database WHERE datname IS NOT NULL",'Le cache OS est absent de ce ratio; interpréter selon la charge.'),
('PER06','Tuples morts',"SELECT schemaname, relname,n_live_tup,n_dead_tup,round(100.0*n_dead_tup/nullif(n_live_tup+n_dead_tup,0),2) AS dead_pct FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 100",'Estimations statistiques; vérifier la fréquence de vacuum.'),
('PER07','Autovacuum',"SELECT schemaname,relname,last_autovacuum,autovacuum_count,last_autoanalyze,autoanalyze_count,n_mod_since_analyze FROM pg_stat_user_tables ORDER BY n_mod_since_analyze DESC LIMIT 100",'Vérifier les seuils et les options par table.'),
('PER08','Index peu utilisés',"SELECT schemaname,relname,indexrelname,idx_scan,pg_relation_size(indexrelid) AS octets FROM pg_stat_user_indexes ORDER BY idx_scan,octets DESC LIMIT 100",'Ne jamais supprimer un index sur ce seul indicateur; vérifier contraintes et période.'),
('PER09','Lectures séquentielles',"SELECT schemaname,relname,seq_scan,seq_tup_read,idx_scan FROM pg_stat_user_tables ORDER BY seq_tup_read DESC LIMIT 100",'Les scans séquentiels peuvent être optimaux.'),
('PER10','Taille des tables',"SELECT schemaname,relname,pg_total_relation_size(relid) AS octets FROM pg_stat_user_tables ORDER BY octets DESC LIMIT 100",'Suivre la croissance et la capacité.'),
('PER11','Fichiers temporaires',"SELECT datname,temp_files,temp_bytes,stats_reset FROM pg_stat_database WHERE datname IS NOT NULL ORDER BY temp_bytes DESC",'Analyser tris et jointures avant de modifier work_mem.'),
('PER12','Configuration mémoire et vacuum',"SELECT name,setting,unit,source,pending_restart FROM pg_settings WHERE name IN ('shared_buffers','work_mem','maintenance_work_mem','effective_cache_size','max_connections','autovacuum','autovacuum_max_workers','autovacuum_vacuum_scale_factor','track_io_timing','shared_preload_libraries') ORDER BY name",'Dimensionner selon RAM et concurrence; aucune valeur universelle.'),
('PER13','Age des transactions',"SELECT datname,age(datfrozenxid) AS age_xid FROM pg_database ORDER BY 2 DESC",'Comparer à autovacuum_freeze_max_age; surveiller le wraparound.'),
('PER14','Vacuum en cours',"SELECT pid,datname,relid,phase,heap_blks_total,heap_blks_scanned FROM pg_stat_progress_vacuum",'Observer la progression sans interrompre la maintenance.'),
('PER15','Deadlocks et rollbacks',"SELECT datname,deadlocks,xact_commit,xact_rollback,stats_reset FROM pg_stat_database WHERE datname IS NOT NULL",'Compteurs cumulatifs: comparer deux captures.'),
('PER16','Options par table',"SELECT n.nspname,c.relname,c.reloptions FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE c.relkind IN ('r','m') AND n.nspname NOT IN ('pg_catalog','information_schema') AND c.reloptions IS NOT NULL LIMIT 100",'Repérer les exceptions aux réglages globaux.'),
('PER17','Statistiques des requêtes',None,'pg_stat_statements doit être installé et préchargé; les identifiants remplacent le texte SQL.'),
('PER18','Sessions idle in transaction',"SELECT pid,extract(epoch FROM now()-state_change)::bigint AS secondes FROM pg_stat_activity WHERE state LIKE 'idle in transaction%' ORDER BY state_change LIMIT 100",'Examiner les transactions laissées ouvertes.'),
]

def query(a, sql):
    env=os.environ.copy(); env['PGOPTIONS']='-c default_transaction_read_only=on -c statement_timeout=10000 -c lock_timeout=2000 -c search_path=pg_catalog'; env['PGCONNECT_TIMEOUT']='5'; env['PGCLIENTENCODING']='UTF8'
    cmd=['psql','-X','-w','-qAt','-v','ON_ERROR_STOP=1','-p',str(a.port),'-d',a.database]
    if a.host: cmd+=['-h',a.host]
    if a.user: cmd+=['-U',a.user]
    # Empêcher l'interprétation du nom de base comme chaîne de connexion.
    if '=' in a.database or a.database.startswith(('postgresql://','postgres://')): raise ValueError('Nom de base invalide')
    wrapped="BEGIN READ ONLY; SELECT coalesce(json_agg(t),'[]'::json) FROM ("+sql+") t; ROLLBACK;"
    r=subprocess.run(cmd+['-c',wrapped],env=env,capture_output=True,text=True,timeout=20,check=True)
    return json.loads(r.stdout)

def collect(a):
    meta=query(a,"SELECT current_database() AS base,current_user AS role,current_setting('server_version') AS version,current_setting('port') AS port,pg_is_in_recovery() AS replica")
    results=[]
    for ident,title,sql,advice in CHECKS:
        try:
            if sql is None:
                ext=query(a,"SELECT n.nspname AS schema FROM pg_extension e JOIN pg_namespace n ON n.oid=e.extnamespace WHERE e.extname='pg_stat_statements'")
                if not ext: raise ValueError('Extension absente dans cette base')
                schema='"'+ext[0]['schema'].replace('"','""')+'"'
                sql=f'SELECT queryid,calls,round(total_exec_time::numeric,2) AS total_ms,round(mean_exec_time::numeric,2) AS mean_ms,rows,shared_blks_read,temp_blks_written FROM {schema}.pg_stat_statements WHERE dbid=(SELECT oid FROM pg_database WHERE datname=current_database()) ORDER BY total_exec_time DESC LIMIT 30'
            rows=query(a,sql); status='OBSERVE'; error=None
        except (ValueError,subprocess.SubprocessError,OSError) as e:
            rows=[]; status='UNKNOWN'; error=type(e).__name__ if not isinstance(e,ValueError) else 'Données indisponibles ou extension absente'
        results.append(dict(id=ident,title=title,status=status,rows=rows,recommendation=advice,error=error))
    return dict(version='1.0.0',date=datetime.datetime.now(datetime.timezone.utc).isoformat(),server=meta,checks=results,limitations='Instantané; visibilité dépend des droits; compteurs cumulatifs; maximum 100 lignes par contrôle (30 pour les requêtes).')

def render(report):
    esc=lambda x:html.escape(str(x))
    sections=[]
    for c in report['checks']:
        rows=c['rows']; keys=list(rows[0]) if rows else []
        table='<table><thead><tr>'+''.join('<th>'+esc(k)+'</th>' for k in keys)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(r.get(k,''))+'</td>' for k in keys)+'</tr>' for r in rows)+'</tbody></table>' if rows else '<p>Aucune ligne visible.</p>'
        sections.append(f'<section><h2>{esc(c["id"])} — {esc(c["title"])}</h2><strong>{esc(c["status"])}</strong><p>{esc(c["recommendation"])}</p><p>{esc(c["error"] or "")}</p>{table}</section>')
    return '<!doctype html><html lang="fr"><meta charset="utf-8"><title>Performance Doctor</title><style>body{font:16px system-ui;color:#183047;background:#f3f6f8;max-width:1200px;margin:auto;padding:24px}header,section{background:white;padding:24px;margin:16px 0;border-radius:8px;overflow:auto}h1,h2{color:#174d68}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:8px;border-bottom:1px solid #ddd;text-align:left}th{background:#e5eef4}</style><header><h1>PostgreSQL Performance Doctor</h1><p>'+esc(report['date'])+'</p><p>'+esc(report['server'])+'</p><p>'+esc(report['limitations'])+'</p></header>'+''.join(sections)+'</html>'

def save(report, output):
    os.umask(0o077); root=pathlib.Path(output); root.mkdir(mode=0o700,parents=True,exist_ok=True)
    if root.is_symlink() or root.stat().st_uid!=os.getuid() or root.stat().st_mode & 0o077: raise ValueError('Répertoire de sortie non privé')
    dest=pathlib.Path(tempfile.mkdtemp(prefix='doctor-',dir=root))
    (dest/'rapport.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8'); (dest/'rapport.html').write_text(render(report),encoding='utf-8'); return dest

def main():
    p=argparse.ArgumentParser(description='Diagnostic PostgreSQL en lecture seule'); p.add_argument('--version',action='version',version='1.0.0'); p.add_argument('--interactive',action='store_true'); p.add_argument('--host'); p.add_argument('--port',type=int,default=5432); p.add_argument('--user'); p.add_argument('--database',default='postgres'); p.add_argument('--output',default=str(pathlib.Path.home()/'performance-reports')); a=p.parse_args()
    try:
        if a.interactive:
            if pathlib.Path('/etc/os-release').exists(): print(next((l for l in pathlib.Path('/etc/os-release').read_text().splitlines() if l.startswith('PRETTY_NAME=')),''))
            if shutil.which('pg_lsclusters'): subprocess.run(['pg_lsclusters'],check=False)
            a.host=input('Hôte ou socket (vide = défaut) : ').strip() or None; a.port=int(input('Port [5432] : ') or '5432'); a.database=input('Base [postgres] : ') or 'postgres'; a.user=input('Rôle (vide = défaut) : ').strip() or None; a.output=input(f'Rapports [{a.output}] : ') or a.output
        if not 1<=a.port<=65535: raise ValueError('Port invalide')
        report=collect(a); print('Rapports :',save(report,a.output)); return 2 if any(c['status']=='UNKNOWN' for c in report['checks']) else 0
    except (ValueError,OSError,subprocess.SubprocessError,EOFError,KeyboardInterrupt) as e: print('Échec du diagnostic :',type(e).__name__); return 1
if __name__=='__main__': raise SystemExit(main())
