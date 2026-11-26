from pathlib import Path
import subprocess
r=Path(__file__).resolve().parents[1]
files=sorted((r/'runbooks').glob('*.md'))
assert len(files)==25
for f in files:
 s=f.read_text(); assert all(x in s for x in ['BEGIN READ ONLY','ROLLBACK','## Validation','## Retour arrière','## Prévention'])
subprocess.run(['bash','-n',str(r/'scripts/diagnostic.sh')],check=True)
assert subprocess.run(['bash',str(r/'scripts/diagnostic.sh'),'65536'],capture_output=True).returncode==2
print('PASS : 25 runbooks, sections, syntaxe Bash, rejet port invalide')
