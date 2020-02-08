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

class TestCsPhonotypeModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mod.start()

    @classmethod
    def tearDownClass(cls):
        run_through_module(End())

    def test_pouze(self):
        word = run_through_module(Text('pouze'))
        self.assertEqual(word.get_text(), 'pouze')
        self.assertEqual(word.get_phonotypes(), [CONS, SUBUNIT, VOWEL, CONS, VOWEL])

    def test_pouzil(self):
        word = run_through_module(Text('použil'))
        self.assertEqual(word.get_text(),'použil')
        self.assertEqual(word.get_phonotypes(), [CONS, VOWEL, VOWEL, CONS, VOWEL, SONOR])

    def test_farmaceuticky(self):
        word = run_through_module(Text('farmaceutický'))
        self.assertEqual(word.get_text(), 'farmaceutický')
        self.assertEqual(word.get_phonotypes(),[CONS, VOWEL, SONOR, SONOR, VOWEL, CONS, SUBUNIT, VOWEL, CONS, VOWEL,
                                                  CONS, CONS, VOWEL])

    def test_neurcity(self):
        word = run_through_module(Text('neurčitý'))
        self.assertEqual(word.get_text(), 'neurčitý')
        self.assertEqual(word.get_phonotypes(), [SONOR, VOWEL, VOWEL, SONOR, CONS, VOWEL, CONS, VOWEL])

    def test_automaticky(self):
        word = run_through_module(Text('automatický'))
        self.assertEqual(word.get_text(), 'automatický')
        self.assertEqual(word.get_phonotypes(), [SUBUNIT, VOWEL, CONS, VOWEL, SONOR, VOWEL, CONS, VOWEL, CONS, CONS,
                                                  VOWEL])

    def test_vlna(self):
        word = run_through_module(Text('vlna'))
        self.assertEqual(word.get_text(), 'vlna')
        self.assertEqual(word.get_phonotypes(), [CONS, VOWEL, SONOR, VOWEL])

    def test_osm(self):
        word = run_through_module(Text('osm'))
        self.assertEqual(word.get_text(), 'osm')
        self.assertEqual(word.get_phonotypes(), [VOWEL, CONS, VOWEL])

    def test_biologie(self):
        word = run_through_module(Text('biologie'))
        self.assertEqual(word.get_text(), 'bijologije')
        self.assertEqual(word.get_phonotypes(),[CONS, VOWEL, SONOR, VOWEL, SONOR, VOWEL, CONS, VOWEL, SONOR, VOWEL])

    def test_srozpadem(self):
        word = run_through_module(Text('srozpadem'))
        self.assertEqual(word.get_text(), 'srozpadem')
        self.assertEqual(word.get_phonotypes(), [CONS, SONOR, VOWEL, CONS, CONS, VOWEL, CONS, VOWEL, SONOR])

    def test_vedomi(self):
        word = run_through_module(Text('vědomí'))
        self.assertEqual(word.get_text(), 'vědomí')
        self.assertEqual(word.get_phonotypes(), [CONS, VOWEL, CONS, VOWEL, SONOR, VOWEL])

    def test_sex(self):
        word = run_through_module(Text('sex'))
        self.assertEqual(word.get_text(), 'sex')
        self.assertEqual(word.get_phonotypes(), [CONS, VOWEL, CONS])

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

data = ConfigData('../../configs/conf_cs_lat.json')
pin = Pipe(Queue(), Condition())
pout = Pipe(Queue(), Condition())
mod = PhonotypeModule([pin, pout], data)

if __name__ == '__main__':
    unittest.main()
