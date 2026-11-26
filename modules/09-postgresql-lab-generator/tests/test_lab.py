import unittest, sys, subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import lab
class TestLab(unittest.TestCase):
    def test_names(self):
        self.assertEqual(lab.name('lab_test'),'lab_test')
        for x in ['postgres','lab_','lab_x;drop','lab_X']:
            with self.assertRaises(Exception): lab.name(x)
    def test_volume(self):
        for x in ['1000','10000000']: self.assertEqual(lab.volume(x),int(x))
        for x in ['999','10000001']:
            with self.assertRaises(Exception): lab.volume(x)
    def test_dry(self):
        r=subprocess.run([sys.executable,str(lab.ROOT/'lab.py'),'create'],capture_output=True,text=True)
        self.assertEqual(r.returncode,0); self.assertIn('SIMULATION',r.stdout)
    def test_invalid_port(self):
        r=subprocess.run([sys.executable,str(lab.ROOT/'lab.py'),'create','--port','0'],capture_output=True)
        self.assertNotEqual(r.returncode,0)
