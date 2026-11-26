#!/usr/bin/env python3
"""Générateur de laboratoires isolés, sans dépendance Python externe."""
import argparse, os, re, subprocess, sys, shlex
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def name(s):
    if not re.fullmatch(r'lab_[a-z0-9_]{1,40}',s): raise argparse.ArgumentTypeError('Nom obligatoire : lab_ suivi de lettres minuscules, chiffres ou _')
    return s

def volume(s):
    n=int(s)
    if not 1000<=n<=10000000: raise argparse.ArgumentTypeError('Volume : 1000 à 10000000')
    return n

def run(cmd):
    print(shlex.join(map(str,cmd)),flush=True)
    subprocess.run(cmd,check=True,env={**os.environ,'PGCONNECT_TIMEOUT':'5'})

def main():
    a=argparse.ArgumentParser(description='PostgreSQL Lab Generator Premium')
    a.add_argument('action',choices=['create','backup','restore','interactive'])
    a.add_argument('--database',type=name,default='lab_dgpc')
    a.add_argument('--rows',type=volume,default=10000)
    a.add_argument('--port',type=int,default=5432)
    a.add_argument('--host',default='/var/run/postgresql')
    a.add_argument('--user')
    a.add_argument('--archive',type=Path)
    a.add_argument('--apply',action='store_true')
    x=a.parse_args()
    if x.action=='interactive':
        print('1. Créer un laboratoire\n2. Sauvegarder\n3. Restaurer dans une nouvelle base\n0. Quitter')
        c=input('Choix : ')
        if c not in ('1','2','3'): return
        x.action={'1':'create','2':'backup','3':'restore'}[c]
        x.database=name(input('Nom lab_ : '))
        x.port=int(input('Port [5432] : ') or '5432')
        if x.action=='create': x.rows=volume(input('Nombre de lignes [10000] : ') or '10000')
        else: x.archive=Path(input('Archive : '))
        x.apply=input('Confirmer sur une instance de formation (OUI) : ')=='OUI'
    if not 1<=x.port<=65535: a.error('Port invalide')
    # Les noms de bases sont strictement contrôlés; aucun shell intermédiaire.
    conn=['-h',x.host,'-p',str(x.port)]+(['-U',x.user] if x.user else [])
    if x.action!='create' and x.archive is None: a.error('--archive obligatoire')
    print(f'Action={x.action} cible={x.host}:{x.port}/{x.database} lignes={x.rows}')
    if not x.apply: print('SIMULATION : aucune modification. Ajouter --apply.'); return
    os.umask(0o077)
    if x.action=='create':
        run(['createdb','-w',*conn,'-T','template0',x.database])
        run(['psql','-X','-w',*conn,'-d',x.database,'-v','ON_ERROR_STOP=1','-v',f'n={x.rows}','-f',str(ROOT/'sql/00_setup.sql')])
    elif x.action=='backup':
        if x.archive.exists(): a.error('Archive existante : refus')
        # Création exclusive, suppression du fichier incomplet en cas d’échec.
        with x.archive.open('xb') as f:
            try: subprocess.run(['pg_dump','-w',*conn,'-Fc','-d',x.database],stdout=f,check=True)
            except BaseException: x.archive.unlink(); raise
        run(['pg_restore','--list',str(x.archive.absolute())])
    else:
        run(['pg_restore','--list',str(x.archive.absolute())])
        run(['createdb','-w',*conn,'-T','template0',x.database])
        run(['pg_restore','-w',*conn,'--exit-on-error','--single-transaction','--no-owner','--no-privileges','-d',x.database,str(x.archive.absolute())])
if __name__=='__main__':
    try: main()
    except (ValueError,OSError,subprocess.CalledProcessError,argparse.ArgumentTypeError) as e: sys.exit(str(e))
