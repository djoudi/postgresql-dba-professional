import unittest,tempfile,json,os
from pathlib import Path
from migrate import endpoint,assess,report,digest
class Tests(unittest.TestCase):
 def test_endpoint(self):
  self.assertIn('service=source',endpoint('source','app'))
  with self.assertRaises(ValueError): endpoint('source','x dbname=y')
 def test_assess(self):
  def inv(v): return {'serveur':dict(version=v,recovery=False,encoding='UTF8',collation='C',ctype='C'),'extensions':[],'extensions_disponibles':[],'roles':[]}
  self.assertFalse(assess(inv(140000),inv(180000))['blocages'])
  self.assertTrue(assess(inv(180000),inv(140000))['blocages'])
 def test_report(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'report'; report(p,{'x':'<script>'}); self.assertIn('&lt;script&gt;', (p/'rapport.html').read_text()); self.assertEqual(json.loads((p/'rapport.json').read_text())['x'],'<script>')
   with self.assertRaises(FileExistsError): report(p,{})
 def test_digest(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'a'; p.write_bytes(b'abc'); self.assertEqual(digest(p),'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
