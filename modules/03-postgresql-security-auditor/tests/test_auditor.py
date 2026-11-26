import unittest,sys,pathlib,argparse
from unittest.mock import patch
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import auditor
class Tests(unittest.TestCase):
 def test_collect(self):
  a=argparse.Namespace(database='postgres',port=5432)
  with patch('auditor.query',side_effect=['180000']+['0']*len(auditor.CHECKS)):
   r=auditor.collect(a)
  self.assertEqual(len(r['checks']),24); self.assertTrue(all(c['status']=='OK' for c in r['checks']))
 def test_unknown(self):
  a=argparse.Namespace(database='postgres',port=5432)
  with patch('auditor.query',side_effect=['180000',RuntimeError()]+['1']*23): r=auditor.collect(a)
  self.assertEqual(r['checks'][0]['status'],'UNKNOWN'); self.assertEqual(r['checks'][1]['status'],'REVIEW')
 def test_escape(self):
  self.assertIn('&lt;script&gt;',auditor.render(dict(database='<script>',generated_at='x',checks=[])))
 def test_readonly(self):
  self.assertTrue(all(c[3].startswith('SELECT ') for c in auditor.CHECKS))
