import pathlib, subprocess, sys, json, os, ast
R=pathlib.Path(__file__).resolve().parents[1]
failed=0
for m in json.loads((R/'modules.json').read_text()):
 d=R/m['path']; print('\n===',m['name'],flush=True)
 for p in d.rglob('*.py'): ast.parse(p.read_text())
 for p in d.rglob('*.sh'): subprocess.run(['bash','-n',str(p)],check=True)
 t=d/'tests'; cmds=[]
 if (t/'check.py').exists():cmds.append([sys.executable,str(t/'check.py')])
 if (t/'smoke.sh').exists():cmds.append(['bash',str(t/'smoke.sh')])
 if list(t.glob('test_*.py')):cmds.append([sys.executable,'-m','unittest','discover','-s','tests','-v'])
 if not cmds: raise RuntimeError('Suite absente: '+str(d))
 for cmd in cmds:
  r=subprocess.run(cmd,cwd=d,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},timeout=60);failed+=bool(r.returncode)
 print('Syntaxe Python/Bash OK; suites exécutées:',len(cmds),flush=True)
print('Suites en échec:',failed);sys.exit(bool(failed))
