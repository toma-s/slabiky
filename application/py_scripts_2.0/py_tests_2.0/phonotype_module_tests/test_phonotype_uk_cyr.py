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

class TestUkPhonotypeModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mod.start()

    @classmethod
    def tearDownClass(cls):
        run_through_module(End())

    def test_стверджує(self):
        word = run_through_module(Text('стверджує'))
        self.assertEqual(word.get_text(), 'стверджує')
        self.assertEqual(word.get_phonotypes(), [OBSTR, OBSTR, GLIDE, VOWEL, LIQUID, SUBUNIT, OBSTR, VOWEL, VOWEL])

    def test_має(self):
        word = run_through_module(Text('має'))
        self.assertEqual(word.get_text(), 'має')
        self.assertEqual(word.get_phonotypes(), [NASAL, VOWEL, VOWEL])

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

data = ConfigData(path_to_scripts + '\configs\conf_uk_cyr.json')
pin = Pipe(Queue(), Condition())
pout = Pipe(Queue(), Condition())
mod = PhonotypeModule([pin, pout], data)

if __name__ == '__main__':
    unittest.main()
