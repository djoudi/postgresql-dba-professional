import unittest,tempfile,pathlib,json,os
from unittest.mock import patch
import health
class TestHealth(unittest.TestCase):
 def sample(self):
  return {'date_utc':'2026-01-01','cible':{'base':'<script>'},'systeme_local':{},'controles':{'bases':{'statut':'OK','lignes':[{'base':'<script>','octets':1024}],'conseil':'Test'}}}
 def test_html(self):
  s=health.render(self.sample()); self.assertIn('&lt;script&gt;',s); self.assertNotIn('<script>',s); self.assertIn('<meter',s)
 def test_export(self):
  with tempfile.TemporaryDirectory() as t:
   p=health.export(self.sample(),t); self.assertEqual(json.loads((p/'rapport.json').read_text()),self.sample()); self.assertEqual((p/'rapport.csv').stat().st_mode & 0o777,0o600)
 def test_unsafe_dir(self):
  with tempfile.TemporaryDirectory() as t:
   os.chmod(t,0o755)
   with self.assertRaises(ValueError): health.export(self.sample(),t)
 def test_collect_failure(self):
  a=type('A',(),dict(host='/tmp',port=5432,database='postgres',user=None))()
  with patch('health.subprocess.run',side_effect=OSError):
   d=health.collect(a); self.assertEqual(len(d['controles']),16); self.assertTrue(all(v['statut']=='UNKNOWN' for v in d['controles'].values()))
if __name__=='__main__': unittest.main()
