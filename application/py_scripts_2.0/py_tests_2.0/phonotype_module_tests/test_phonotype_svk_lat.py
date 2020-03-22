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

class TestSlPhonotypeModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mod.start()

    @classmethod
    def tearDownClass(cls):
        run_through_module(End())

    def test_vlna(self):
        word = run_through_module(Text('vlna'))
        self.assertEqual(word.get_text(), 'vlna')
        self.assertEqual(word.get_phonotypes(), [OBSTR, VOWEL, NASAL, VOWEL])

    def test_vlca(self):
        word = run_through_module(Text('vĺča'))
        self.assertEqual(word.get_text(), 'vĺča')
        self.assertEqual(word.get_phonotypes(), [OBSTR, VOWEL, OBSTR, VOWEL])

    def test_zmrzlina(self):
        word = run_through_module(Text('zmrzlina'))
        self.assertEqual(word.get_text(), 'zmrzlina')
        self.assertEqual(word.get_phonotypes(), [OBSTR, NASAL, VOWEL, OBSTR, LIQUID, VOWEL, NASAL, VOWEL])

    def test_vrba(self):
        word = run_through_module(Text('vŕba'))
        self.assertEqual(word.get_text(), 'vŕba')
        self.assertEqual(word.get_phonotypes(), [OBSTR, VOWEL, OBSTR, VOWEL])


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

data = ConfigData(path_to_scripts + '\configs\conf_svk_lat.json')
pin = Pipe(Queue(), Condition())
pout = Pipe(Queue(), Condition())
mod = PhonotypeModule([pin, pout], data)

if __name__ == '__main__':
    unittest.main()
