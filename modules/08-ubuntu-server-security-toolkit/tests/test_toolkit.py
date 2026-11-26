import unittest, tempfile, pathlib, json
from unittest.mock import patch
import toolkit
class Tests(unittest.TestCase):
    def test_profile(self):
        self.assertIn('PermitRootLogin no',toolkit.profile()); self.assertNotIn('PasswordAuthentication no',toolkit.profile())
    @patch('toolkit.run')
    def test_dry(self,r):
        toolkit.harden(False); toolkit.action(['ufw','allow'],False); r.assert_not_called()
    @patch('toolkit.run')
    def test_audit(self,r):
        r.return_value.returncode=0; r.return_value.stdout='<script>test</script>'
        with tempfile.TemporaryDirectory() as d:
            toolkit.audit(d); p=next(pathlib.Path(d).iterdir()); self.assertEqual(len(json.loads((p/'rapport.json').read_text())),12); self.assertIn('&lt;script&gt;', (p/'rapport.html').read_text()); self.assertEqual((p/'rapport.json').stat().st_mode & 0o777,0o600)
if __name__=='__main__': unittest.main()
