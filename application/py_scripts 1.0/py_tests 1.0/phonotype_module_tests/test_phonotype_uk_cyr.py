from pipe import Pipe
from queue import Queue
from threading import Condition
from phonotype_module import PhonotypeModule
from word import Text, TextPhonotypes
from constants import SONOR, CONS, VOWEL, SPEC, SUBUNIT
from end import End
from config_data import ConfigData
from pathlib import Path
import unittest

class TestUkPhonotypeModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mod.start()

    @classmethod
    def tearDownClass(cls):
        run_through_module(End())

    def test_українськогож(self):
        word = run_through_module(Text('українськогож'))
        self.assertEqual(word.get_text(), 'українськогож')
        self.assertEqual(word.get_phonotypes(), [VOWEL, CONS, SONOR, VOWEL, VOWEL, SONOR, CONS, SPEC, CONS, VOWEL, CONS,
                                                 VOWEL, CONS])

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

data = ConfigData('../../configs/conf_uk_cyr.json')
pin = Pipe(Queue(), Condition())
pout = Pipe(Queue(), Condition())
mod = PhonotypeModule([pin, pout], data)

if __name__ == '__main__':
    unittest.main()
