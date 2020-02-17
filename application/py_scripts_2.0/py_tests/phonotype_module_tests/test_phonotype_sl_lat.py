import sys

path_to_scripts = 'C:/Users/palo/Desktop/slabiky-master/application/py_scripts 2.0'
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

class TestSlPhonotypeModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mod.start()

    @classmethod
    def tearDownClass(cls):
        run_through_module(End())

    def test_crni(self):
        word = run_through_module(Text('črni'))
        self.assertEqual(word.get_text(), 'črni')
        self.assertEqual(word.get_phonotypes(), [OBSTR, VOWEL, NASAL, VOWEL])

    def test_rz(self):
        word = run_through_module(Text('rž'))
        self.assertEqual(word.get_text(), 'rž')
        self.assertEqual(word.get_phonotypes(), [VOWEL, OBSTR])

    def test_rza(self):
        word = run_through_module(Text('rža'))
        self.assertEqual(word.get_text(), 'rža')
        self.assertEqual(word.get_phonotypes(), [LIQUID, OBSTR, VOWEL])

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

data = ConfigData(path_to_scripts + '\configs\conf_sl_lat.json')
pin = Pipe(Queue(), Condition())
pout = Pipe(Queue(), Condition())
mod = PhonotypeModule([pin, pout], data)

if __name__ == '__main__':
    unittest.main()
