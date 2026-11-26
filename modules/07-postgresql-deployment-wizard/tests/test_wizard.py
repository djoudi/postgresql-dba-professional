import unittest
from unittest.mock import patch
import wizard
class Tests(unittest.TestCase):
 def test_memory(self):
  self.assertEqual(wizard.tuning(4096)['shared_buffers'],'1024MB')
 def test_cap(self):
  self.assertEqual(wizard.tuning(65536)['shared_buffers'],'8192MB')
 def test_invalid(self):
  for v,c in [(13,'main'),(18,'../main'),(18,'a;b')]:
   with self.assertRaises(ValueError): wizard.valid(v,c)
 def test_dry_run(self):
  with patch('subprocess.run') as r:
   wizard.run(['apt-get','install','postgresql-18']); r.assert_not_called()
 def test_apply(self):
  with patch('subprocess.run') as r:
   wizard.run(['true'],True); r.assert_called_once()
