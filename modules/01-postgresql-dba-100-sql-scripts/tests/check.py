from pathlib import Path
p=Path(__file__).resolve().parents[1]
files=list(p.glob("*/*.sql"))
assert len(files)==100
for f in files:
 s=f.read_text(); assert "BEGIN READ ONLY;" in s and s.endswith("ROLLBACK;\n"), f
print("100 fichiers : contrôle structurel OK")
