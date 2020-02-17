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

class TestUkPhonotypeModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mod.start()

    @classmethod
    def tearDownClass(cls):
        run_through_module(End())

    def test_шестое(self):
        word = run_through_module(Text('шестое'))
        self.assertEqual(word.get_text(), 'шестое')
        self.assertEqual(word.get_phonotypes(), [OBSTR, VOWEL, OBSTR, OBSTR, VOWEL, VOWEL])

    def test_объёму(self):
        word = run_through_module(Text('объёму'))
        self.assertEqual(word.get_text(), 'объёму')
        self.assertEqual(word.get_phonotypes(), [VOWEL, OBSTR, SPEC, VOWEL, NASAL, VOWEL])

    def test_россия(self):
        word = run_through_module(Text('россия'))
        self.assertEqual(word.get_text(), 'россия')
        self.assertEqual(word.get_phonotypes(), [LIQUID, VOWEL, OBSTR, OBSTR, VOWEL, VOWEL])

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

data = ConfigData(path_to_scripts + '\configs\conf_ru_cyr.json')
pin = Pipe(Queue(), Condition())
pout = Pipe(Queue(), Condition())
mod = PhonotypeModule([pin, pout], data)

if __name__ == '__main__':
    unittest.main()
