#!/usr/bin/env python3
"""Lanceur unifié : aucune élévation ni modification implicite."""
import json, pathlib, shutil, subprocess, sys, shlex
R=pathlib.Path(__file__).resolve().parent
M=json.loads((R/'modules.json').read_text())
def main():
 if len(sys.argv)>1 and sys.argv[1]=='--check':
  for c in ['python3','bash','psql','pg_dump','pg_restore','createdb','pg_lsclusters','systemctl','sshd','ufw','fail2ban-client']:
   print(f'{c:20} {shutil.which(c) or "ABSENT (selon module)"}')
  return
 while True:
  print('\n=== PostgreSQL DBA Professional Pack 2026 | Ultimate ===')
  for m in M: print(f"{m['id']:2} | {m['name']}")
  print(' 0 | Quitter')
  try: choice=int(input('Module : '))
  except (ValueError,EOFError): return
  if choice==0:return
  if not 1<=choice<=len(M):continue
  m=M[choice-1]; d=R/m['path']; print('Documentation :',d/'README.md')
  if not m['entry']: print('Bibliothèque SQL : choisir un fichier et le lire avant exécution.');continue
  print('Entrée :',m['entry']); print('Consulter README. Les commandes natives peuvent modifier le système.')
  try: args=shlex.split(input('Arguments (vide = annuler) : '))
  except (ValueError,EOFError):continue
  if not args:continue
  cmd=['bash',str(d/m['entry']),*args]; print(shlex.join(cmd))
  if input('Exécuter cette commande ? (OUI) : ')=='OUI': print('Code retour :',subprocess.call(cmd,cwd=d))
if __name__=='__main__':main()
