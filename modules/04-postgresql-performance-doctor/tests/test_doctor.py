import unittest, tempfile, pathlib, argparse, subprocess
from unittest.mock import patch
import doctor
class Tests(unittest.TestCase):
    def test_collect(self):
        with patch('doctor.query',side_effect=lambda a,s: []):
            r=doctor.collect(None)
        self.assertEqual(len(r['checks']),18)
        self.assertEqual(r['checks'][16]['status'],'UNKNOWN')
    def test_escape(self):
        r={'date':'<script>','server':[],'limitations':'x','checks':[]}
        self.assertNotIn('<script>',doctor.render(r))
    def test_save(self):
        with tempfile.TemporaryDirectory() as d:
            p=doctor.save({'date':'x','server':[],'limitations':'x','checks':[]},d)
            self.assertTrue((p/'rapport.json').exists()); self.assertEqual((p/'rapport.html').stat().st_mode & 0o777,0o600)
    def test_readonly(self):
        a=argparse.Namespace(port=5432,database='postgres',host=None,user=None)
        with patch('doctor.subprocess.run',return_value=subprocess.CompletedProcess([],0,'[]','')) as run:
            doctor.query(a,'SELECT 1')
            self.assertIn('BEGIN READ ONLY',run.call_args.args[0][-1]); self.assertIn('statement_timeout=10000',run.call_args.kwargs['env']['PGOPTIONS'])
    def test_conninfo(self):
        a=argparse.Namespace(port=5432,database='host=other',host=None,user=None)
        with self.assertRaises(ValueError): doctor.query(a,'SELECT 1')
if __name__=='__main__': unittest.main()
