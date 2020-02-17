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

class TestHsbPhonotypeModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mod.start()

    @classmethod
    def tearDownClass(cls):
        run_through_module(End())

    def test_kupje(self):
        word = run_through_module(Text('kupje'))
        self.assertEqual(word.get_text(), 'kupje')
        self.assertEqual(word.get_phonotypes(), [OBSTR, VOWEL, SUBUNIT, OBSTR, VOWEL])

    def test_chosebuz(self):
        word = run_through_module(Text('chóśebuz'))
        self.assertEqual(word.get_text(), 'chóśebuz')
        self.assertEqual(word.get_phonotypes(), [SUBUNIT, OBSTR, VOWEL, OBSTR, VOWEL, OBSTR, VOWEL, OBSTR])

    def test_zajtso(self):
        word = run_through_module(Text('zajtšo'))
        self.assertEqual(word.get_text(), 'zajtšo')
        self.assertEqual(word.get_phonotypes(), [OBSTR, VOWEL, GLIDE, SUBUNIT, OBSTR, VOWEL])

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

data = ConfigData(path_to_scripts + '\configs\conf_dsb_lat.json')
pin = Pipe(Queue(), Condition())
pout = Pipe(Queue(), Condition())
mod = PhonotypeModule([pin, pout], data)

if __name__ == '__main__':
    unittest.main()
