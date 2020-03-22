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

    def test_vlna(self):
        word = run_through_module(Text('vlna'))
        self.assertEqual(word.get_text(), 'vlna')
        self.assertEqual(word.get_phonotypes(), [OBSTR, VOWEL, NASAL, VOWEL])

    def test_vrba(self):
        word = run_through_module(Text('vrba'))
        self.assertEqual(word.get_text(),'vrba')
        self.assertEqual(word.get_phonotypes(), [OBSTR, VOWEL, OBSTR, VOWEL])

    def test_sedm(self):
        word = run_through_module(Text('sedm'))
        self.assertEqual(word.get_text(), 'sedm')
        self.assertEqual(word.get_phonotypes(),[OBSTR, VOWEL, OBSTR, VOWEL])

    def test_osm(self):
        word = run_through_module(Text('osm'))
        self.assertEqual(word.get_text(), 'osm')
        self.assertEqual(word.get_phonotypes(), [VOWEL, OBSTR, VOWEL])

    def test_sedmou(self):
        word = run_through_module(Text('sedmou'))
        self.assertEqual(word.get_text(), 'sedmou')
        self.assertEqual(word.get_phonotypes(), [OBSTR, VOWEL, OBSTR, NASAL, SUBUNIT, VOWEL])

    def test_biologie(self):
        word = run_through_module(Text('biologie'))
        self.assertEqual(word.get_text(), 'bijologije')
        self.assertEqual(word.get_phonotypes(), [OBSTR, VOWEL, GLIDE, VOWEL, LIQUID, VOWEL, OBSTR, VOWEL, GLIDE, VOWEL])

    def test_automatický(self):
        word = run_through_module(Text('automatický'))
        self.assertEqual(word.get_text(), 'automatický')
        self.assertEqual(word.get_phonotypes(),
                         [SUBUNIT, VOWEL, OBSTR, VOWEL, NASAL, VOWEL, OBSTR, VOWEL, OBSTR, OBSTR, VOWEL])

    def test_poucka(self):
        word = run_through_module(Text('poučka'))
        self.assertEqual(word.get_text(), 'poučka')
        self.assertEqual(word.get_phonotypes(), [OBSTR, VOWEL, VOWEL, OBSTR, OBSTR, VOWEL])

    def test_pouze(self):
        word = run_through_module(Text('pouze'))
        self.assertEqual(word.get_text(), 'pouze')
        self.assertEqual(word.get_phonotypes(), [OBSTR, SUBUNIT, VOWEL, OBSTR, VOWEL])

    def test_euforie(self):
        word = run_through_module(Text('euforie'))
        self.assertEqual(word.get_text(), 'euforije')
        self.assertEqual(word.get_phonotypes(), [SUBUNIT, VOWEL, OBSTR, VOWEL, LIQUID, VOWEL, GLIDE, VOWEL])

    def test_neurcity(self):
        word = run_through_module(Text('neurčitý'))
        self.assertEqual(word.get_text(), 'neurčitý')
        self.assertEqual(word.get_phonotypes(), [NASAL, VOWEL, VOWEL, LIQUID, OBSTR, VOWEL, OBSTR, VOWEL])

    def test_metr(self):
        word = run_through_module(Text('metr'))
        self.assertEqual(word.get_text(), 'metr')
        self.assertEqual(word.get_phonotypes(), [NASAL, VOWEL, OBSTR, VOWEL])

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

data = ConfigData(path_to_scripts + '/configs/conf_cs_lat.json')
pin = Pipe(Queue(), Condition())
pout = Pipe(Queue(), Condition())
mod = PhonotypeModule([pin, pout], data)

if __name__ == '__main__':
    unittest.main()
