#!/usr/bin/env python3
"""Inventaire et diagnostic PostgreSQL en lecture seule."""
import argparse, csv, datetime, html, json, os, pathlib, shutil, subprocess, sys, tempfile
VERSION='1.0.0'
CHECKS={
 'serveur':("SELECT version() AS version, current_database() AS base, pg_is_in_recovery() AS replica, pg_postmaster_start_time() AS demarrage",'Vérifier la version et le rôle du serveur.'),
 'bases':("SELECT datname AS base, pg_database_size(datname) AS octets FROM pg_database WHERE datallowconn AND has_database_privilege(datname,'CONNECT') ORDER BY 2 DESC",'Surveiller la croissance et la capacité.'),
 'connexions':("SELECT count(*) FILTER (WHERE backend_type='client backend') AS clients, current_setting('max_connections')::int AS maximum, count(*) FILTER (WHERE state='idle in transaction') AS inactives_transaction FROM pg_stat_activity",'Examiner la saturation et le pool de connexions.'),
 'cache':("SELECT datname AS base, round(100.0*blks_hit/nullif(blks_hit+blks_read,0),2) AS ratio_pct, temp_bytes, deadlocks, stats_reset FROM pg_stat_database WHERE datname=current_database()",'Ratio cumulatif du cache PostgreSQL, hors cache OS.'),
 'verrous':("SELECT pid, pg_blocking_pids(pid) AS bloqueurs, wait_event FROM pg_stat_activity WHERE cardinality(pg_blocking_pids(pid))>0",'Identifier les transactions bloquantes sans les terminer.'),
 'transactions':("SELECT pid, extract(epoch FROM now()-xact_start)::bigint AS secondes, state FROM pg_stat_activity WHERE xact_start < now()-interval '5 minutes' AND pid<>pg_backend_pid() ORDER BY 2 DESC LIMIT 50",'Justifier les transactions longues.'),
 'tables':("SELECT schemaname, relname, pg_total_relation_size(relid) AS octets, n_live_tup, n_dead_tup, last_autovacuum, last_autoanalyze FROM pg_stat_user_tables ORDER BY 3 DESC LIMIT 50",'Examiner les estimations et la fréquence de maintenance.'),
 'index':("SELECT schemaname, relname, indexrelname, idx_scan, pg_relation_size(indexrelid) AS octets FROM pg_stat_user_indexes ORDER BY 5 DESC LIMIT 50",'Un index peu utilisé ne doit pas être supprimé sans analyse.'),
 'configuration':("SELECT name, setting, unit, pending_restart FROM pg_settings WHERE name IN ('shared_buffers','work_mem','maintenance_work_mem','effective_cache_size','autovacuum','ssl','password_encryption','listen_addresses','max_connections','archive_mode','track_counts') ORDER BY name",'Comparer les paramètres aux besoins et à la politique locale.'),
 'roles':("SELECT count(*) FILTER (WHERE rolsuper) AS superutilisateurs, count(*) FILTER (WHERE rolcanlogin) AS comptes_login, count(*) FILTER (WHERE rolbypassrls) AS bypass_rls FROM pg_roles",'Justifier les privilèges élevés.'),
 'hba':("SELECT count(*) FILTER (WHERE auth_method='trust') AS trust, count(*) FILTER (WHERE error IS NOT NULL) AS erreurs FROM pg_hba_file_rules",'Examiner les règles trust et les erreurs; accès privilégié requis.'),
 'tls':("SELECT count(*) FILTER (WHERE s.ssl) AS tls, count(*) FILTER (WHERE NOT s.ssl) AS sans_tls FROM pg_stat_ssl s JOIN pg_stat_activity a USING(pid) WHERE a.client_addr IS NOT NULL",'Vérifier le chiffrement des connexions TCP.'),
 'gel':("SELECT datname AS base, age(datfrozenxid) AS age_xid FROM pg_database ORDER BY 2 DESC",'Comparer à autovacuum_freeze_max_age.'),
 'archivage':("SELECT archived_count, failed_count, last_archived_time, last_failed_time, stats_reset FROM pg_stat_archiver",'Les compteurs sont cumulatifs; vérifier la politique de reprise.'),
 'replication':("SELECT state, sync_state, pg_wal_lsn_diff(sent_lsn,replay_lsn) AS retard_octets FROM pg_stat_replication",'Une absence de lignes ne prouve pas une panne.'),
 'vacuum':("SELECT pid, phase, heap_blks_total, heap_blks_scanned FROM pg_stat_progress_vacuum",'Inventaire instantané des opérations VACUUM.')}

def command(args):
    try:
        p=subprocess.run(args,capture_output=True,text=True,timeout=15,check=True)
        return {'statut':'OK','texte':p.stdout.strip()}
    except (OSError,subprocess.SubprocessError): return {'statut':'UNKNOWN','texte':'Commande indisponible ou accès refusé'}

def collect(a):
    env=os.environ.copy(); env.update(PGOPTIONS='-c default_transaction_read_only=on -c statement_timeout=10000 -c lock_timeout=2000 -c search_path=pg_catalog',PGCONNECT_TIMEOUT='5')
    for k in ('PGSERVICE','PGSERVICEFILE','PGDATABASE','PGHOSTADDR','PGCLUSTER'): env.pop(k,None)
    cmd=['psql','-X','-w','-qAt','-v','ON_ERROR_STOP=1','-h',a.host,'-p',str(a.port),'-d',a.database]
    if a.user: cmd+=['-U',a.user]
    result={}
    for key,(sql,advice) in CHECKS.items():
        try:
            p=subprocess.run(cmd+['-c',"BEGIN READ ONLY; SELECT coalesce(json_agg(t),'[]'::json) FROM ("+sql+") t; ROLLBACK;"],env=env,capture_output=True,text=True,timeout=20,check=True)
            rows=json.loads(p.stdout); result[key]={'statut':'OK','lignes':rows,'conseil':advice}
        except (OSError,subprocess.SubprocessError,ValueError): result[key]={'statut':'UNKNOWN','lignes':[],'conseil':advice+' Collecte impossible; vérifier connexion, version et droits.'}
    return {'version':VERSION,'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cible':{'hote':a.host,'port':a.port,'base':a.database},'systeme_local':{k:command(v) for k,v in {'os':['cat','/etc/os-release'],'noyau':['uname','-sr'],'memoire':['free','-b'],'disques':['df','-hP'],'clusters':['pg_lsclusters'],'charge':['uptime']}.items()},'controles':result}

def render(d):
    e=lambda x:html.escape(str(x),quote=True)
    parts=['<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>PostgreSQL Health Report</title><style>body{font:16px system-ui;background:#eef3f8;color:#183047;margin:0}main{max-width:1100px;margin:auto;padding:24px}header{background:#17354d;color:white;padding:24px;border-radius:12px}section{background:white;padding:20px;margin:16px 0;border-radius:10px;overflow:auto}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:9px;border-bottom:1px solid #ddd;text-align:left}meter{width:65%;height:24px}pre{white-space:pre-wrap}small{color:#536779}</style><main><header><h1>PostgreSQL Health Report — Premium</h1><p>'+e(d['date_utc'])+' | '+e(d['cible'])+'</p></header><section><h2>Synthèse de collecte</h2>']
    checks=d['controles']; ok=sum(x['statut']=='OK' for x in checks.values()); parts.append(f'<p>{ok}/{len(checks)} contrôles collectés (pas un score de santé).</p><meter min="0" max="{len(checks)}" value="{ok}"></meter>')
    rows=checks.get('bases',{}).get('lignes',[]); maximum=max([r['octets'] for r in rows]+[1]); parts.append('<h2>Volumes des bases — échelle relative</h2>')
    for r in rows: parts.append(f'<p>{e(r["base"])} — {r["octets"]/1048576:.2f} Mio<br><meter min="0" max="{maximum}" value="{r["octets"]}"></meter></p>')
    for key,col,maxkey in [('connexions','clients','maximum'),('cache','ratio_pct',None)]:
        rr=checks.get(key,{}).get('lignes',[])
        if rr and rr[0].get(col) is not None:
            val=rr[0][col]; mx=rr[0][maxkey] if maxkey else 100; parts.append(f'<p>{e(key)} : {e(val)} / {e(mx)}<br><meter min="0" max="{mx}" value="{min(val,mx)}"></meter></p>')
    parts.append('</section>')
    for k,v in checks.items():
        parts.append(f'<section><h2>{e(k)} — {e(v["statut"])}</h2><p>{e(v["conseil"])}</p>'); rows=v['lignes']
        if rows:
            cols=list(rows[0]); parts.append('<table><tr>'+''.join('<th>'+e(c)+'</th>' for c in cols)+'</tr>'); parts.extend('<tr>'+''.join('<td>'+e(r.get(c,''))+'</td>' for c in cols)+'</tr>' for r in rows); parts.append('</table>')
        else: parts.append('<p>Aucune ligne collectée.</p>')
        parts.append('</section>')
    parts.append('<section><h2>Machine exécutant le rapport (pas nécessairement le serveur distant)</h2>')
    for k,v in d['systeme_local'].items(): parts.append('<h3>'+e(k)+'</h3><pre>'+e(v['texte'])+'</pre>')
    return ''.join(parts)+'</section></main></html>'

def export(d,output):
    os.umask(0o077); root=pathlib.Path(output).expanduser(); root.mkdir(parents=True,exist_ok=True,mode=0o700)
    if root.is_symlink() or root.stat().st_uid!=os.getuid() or root.stat().st_mode & 0o077: raise ValueError('Répertoire privé 0700 requis')
    folder=pathlib.Path(tempfile.mkdtemp(prefix='health-',dir=root)); (folder/'rapport.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8'); (folder/'rapport.html').write_text(render(d),encoding='utf8')
    with (folder/'rapport.csv').open('w',encoding='utf8',newline='') as f:
        w=csv.writer(f); w.writerow(['controle','statut','ligne_json','conseil'])
        for k,v in d['controles'].items():
            for r in v['lignes'] or [{}]: w.writerow([k,v['statut'],json.dumps(r,ensure_ascii=False),v['conseil']])
    return folder

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--version',action='version',version=VERSION); p.add_argument('--interactive',action='store_true'); p.add_argument('--host',default='/var/run/postgresql'); p.add_argument('--port',type=int,default=5432); p.add_argument('--database',default='postgres'); p.add_argument('--user'); p.add_argument('--output',default='~/health-reports'); a=p.parse_args()
    if a.interactive:
        print(command(['pg_lsclusters'])['texte']); a.host=input(f'Hôte/socket [{a.host}]: ') or a.host; a.port=int(input(f'Port [{a.port}]: ') or a.port); a.database=input('Base [postgres]: ') or a.database; a.user=input('Rôle [courant]: ') or a.user; a.output=input('Répertoire [~/health-reports]: ') or a.output
    if not 1<=a.port<=65535 or not a.database or any(c in a.database for c in '=:/') or ',' in a.host: p.error('Cible invalide')
    if not shutil.which('psql'): p.error('Client psql absent')
    d=collect(a); print(export(d,a.output)); return 1 if d['controles']['serveur']['statut']!='OK' else 2 if any(v['statut']!='OK' for v in d['controles'].values()) else 0
if __name__=='__main__':
    try: sys.exit(main())
    except (ValueError,OSError,EOFError) as exc: print('Erreur:',exc,file=sys.stderr); sys.exit(1)
