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

class TestHsbPhonotypeModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mod.start()

    @classmethod
    def tearDownClass(cls):
        run_through_module(End())

    def test_wrobl(self):
        word = run_through_module(Text('wrobl'))
        self.assertEqual(word.get_text(), 'wrobl')
        self.assertEqual(word.get_phonotypes(), [GLIDE, LIQUID, VOWEL, OBSTR, VOWEL])

    def test_hasa(self):
        word = run_through_module(Text('hasa'))
        self.assertEqual(word.get_text(), 'hasa')
        self.assertEqual(word.get_phonotypes(), [OBSTR, VOWEL, OBSTR, VOWEL])

    def test_hlos(self):
        word = run_through_module(Text('hłós'))
        self.assertEqual(word.get_text(), 'hłós')
        self.assertEqual(word.get_phonotypes(), [OBSTR, GLIDE, VOWEL, OBSTR])

    def test_sahac(self):
        word = run_through_module(Text('sahać'))
        self.assertEqual(word.get_text(), 'sahać')
        self.assertEqual(word.get_phonotypes(), [OBSTR, VOWEL, OBSTR, VOWEL, OBSTR])

    def test_sneh(self):
        word = run_through_module(Text('sněh'))
        self.assertEqual(word.get_text(), 'sněh')
        self.assertEqual(word.get_phonotypes(), [OBSTR, NASAL, VOWEL, OBSTR])

    def test_cahnyc(self):
        word = run_through_module(Text('ćahnyć'))
        self.assertEqual(word.get_text(), 'ćahnyć')
        self.assertEqual(word.get_phonotypes(), [OBSTR, VOWEL, OBSTR, NASAL, VOWEL, OBSTR])

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

data = ConfigData(path_to_scripts + '\configs\conf_hsb_lat.json')
pin = Pipe(Queue(), Condition())
pout = Pipe(Queue(), Condition())
mod = PhonotypeModule([pin, pout], data)

if __name__ == '__main__':
    unittest.main()
