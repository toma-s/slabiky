import sys

path_to_scripts = 'path/slabiky-master/application/py_scripts_2.0'
sys.path.insert(1, path_to_scripts)

from pipe import Pipe
from queue import Queue
from threading import Condition
from phonotype_module import PhonotypeModule
from word import Text, TextPhonotypes
from constants import OBSTR, NASAL, LIQUID, VOWEL, GLIDE, SPEC, SUBUNIT
from end import End
from config_data import ConfigData
import unittest

class TestCsPhonotypeModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mod.start()

    @classmethod
    def tearDownClass(cls):
        run_through_module(End())

    def test_crni(self):
        word = run_through_module(Text('crni'))
        self.assertEqual(word.get_text(), 'crni')
        self.assertEqual(word.get_phonotypes(), [OBSTR, VOWEL, NASAL, VOWEL])

    def test_masakr(self):
        word = run_through_module(Text('masakr'))
        self.assertEqual(word.get_text(),'masakr')
        self.assertEqual(word.get_phonotypes(), [NASAL, VOWEL, OBSTR, VOWEL, OBSTR, VOWEL])

    def test_strjelica(self):
        word = run_through_module(Text('strjelica'))
        self.assertEqual(word.get_text(), 'strjelica')
        self.assertEqual(word.get_phonotypes(),[OBSTR, OBSTR, LIQUID, GLIDE, VOWEL, LIQUID, VOWEL, OBSTR, VOWEL])

    def test_strvelica(self):
        word = run_through_module(Text('strvelica'))
        self.assertEqual(word.get_text(), 'strvelica')
        self.assertEqual(word.get_phonotypes(),[OBSTR, OBSTR, VOWEL, GLIDE, VOWEL, LIQUID, VOWEL, OBSTR, VOWEL])

    def test_njegov(self):
        word = run_through_module(Text('njegov'))
        self.assertEqual(word.get_text(), 'njegov')
        self.assertEqual(word.get_phonotypes(), [SUBUNIT, NASAL, VOWEL, OBSTR, VOWEL, GLIDE])

    def test_rijeka(self):
        word = run_through_module(Text('rijeka'))
        self.assertEqual(word.get_text(), 'rijeka')
        self.assertEqual(word.get_phonotypes(), [LIQUID, SUBUNIT, SUBUNIT, VOWEL, OBSTR, VOWEL])

    def test_derivacija(self):
        word = run_through_module(Text('derivacija'))
        self.assertEqual(word.get_text(), 'derivacija')
        self.assertEqual(word.get_phonotypes(), [OBSTR, VOWEL, LIQUID, VOWEL, GLIDE, VOWEL, OBSTR, VOWEL, GLIDE, VOWEL])

    def test_integral(self):
        word = run_through_module(Text('integral'))
        self.assertEqual(word.get_text(), 'integral')
        self.assertEqual(word.get_phonotypes(), [VOWEL, NASAL, OBSTR, VOWEL, OBSTR, LIQUID, VOWEL, LIQUID])

def run_through_module(word):
    pin.acquire()
    pin.put(word)
    pin.notify()
    pin.release()
    pout.acquire()
    if pout.empty():
        pout.wait()
    word = pout.get()
    pout.release()
    return word

print(path_to_scripts + '/configs/conf_hr_lat.json')

data = ConfigData(path_to_scripts + '/configs/conf_hr_lat.json')

pin = Pipe(Queue(), Condition())
pout = Pipe(Queue(), Condition())
mod = PhonotypeModule([pin, pout], data)

if __name__ == '__main__':
    unittest.main()
