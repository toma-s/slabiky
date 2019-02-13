from config_data import ConfigData
from pipe import Pipe
from queue import Queue
from threading import Condition
from count_module import CountModule
from word import SyllablesPhonotypes
from constants import SONOR, CONS, VOWEL, SPEC, SUBUNIT
from end import End
import unittest

class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mod.start()

    @classmethod
    def tearDownClass(cls):
        run_through_module(End())

    def test_farmaceuticky(self):
        word = run_through_module(SyllablesPhonotypes(['fa', 'rma', 'ceu', 'ti', 'cký'],
                                                      [[CONS, VOWEL], [SONOR, SONOR, VOWEL], [CONS, SUBUNIT, VOWEL],
                                                       [CONS, VOWEL], [CONS, CONS, VOWEL]]))
        self.assertEqual(word.get_syllables(), ['fa', 'rma', 'ceu', 'ti', 'cký'])
        self.assertEqual(word.get_lengths(), [2, 3, 2, 2, 3])

    def test_pouze(self):
        word = run_through_module(SyllablesPhonotypes(['pou', 'ze'], [[CONS, SUBUNIT, VOWEL], [CONS, VOWEL]]))
        self.assertEqual(word.get_syllables(), ['pou', 'ze'])
        self.assertEqual(word.get_lengths(), [2, 2])

    def test_pouzil(self):
        word = run_through_module(SyllablesPhonotypes(['po', 'u', 'žil'], [[CONS, VOWEL], [VOWEL], [CONS, VOWEL, SONOR]]))
        self.assertEqual(word.get_syllables(),['po', 'u', 'žil'])
        self.assertEqual(word.get_lengths(),[2, 1, 3])

    def test_neurcity(self):
        word = run_through_module(SyllablesPhonotypes(['ne', 'ur', 'či', 'tý'],
                                                      [[SONOR, VOWEL], [VOWEL, SONOR], [CONS, VOWEL], [CONS, VOWEL]]))
        self.assertEqual(word.get_syllables(), ['ne', 'ur', 'či', 'tý'])
        self.assertEqual(word.get_lengths(), [2, 2, 2, 2])

    def test_automaticky(self):
        word = run_through_module(SyllablesPhonotypes(['au', 'to', 'ma', 'ti', 'cký'],
                                                      [[SUBUNIT, VOWEL], [CONS, VOWEL], [SONOR, VOWEL],
                                                       [CONS, VOWEL], [CONS, CONS, VOWEL]]))
        self.assertEqual(word.get_syllables(), ['au', 'to', 'ma', 'ti', 'cký'])
        self.assertEqual(word.get_lengths(), [1, 2, 2, 2, 3])

    def test_vlna(self):
        word = run_through_module(SyllablesPhonotypes(['vl', 'na'], [[CONS, VOWEL], [SONOR, VOWEL]]))
        self.assertEqual(word.get_syllables(), ['vl', 'na'])
        self.assertEqual(word.get_lengths(), [2, 2])

    def test_osm(self):
        word = run_through_module(SyllablesPhonotypes(['o', 'sm'], [[VOWEL], [CONS, VOWEL]]))
        self.assertEqual(word.get_syllables(), ['o', 'sm'])
        self.assertEqual(word.get_lengths(), [1, 2])

    def test_bijologije(self):
        word = run_through_module(SyllablesPhonotypes(['bi', 'jo', 'lo', 'gi', 'je'], [[CONS, VOWEL], [SONOR, VOWEL], [SONOR, VOWEL],
                                                                     [CONS, VOWEL], [SONOR, VOWEL]]))
        self.assertEqual(word.get_syllables(), ['bi', 'jo', 'lo', 'gi', 'je'])
        self.assertEqual(word.get_lengths(), [2, 2, 2, 2, 2])

    def test_srozpadem(self):
        word = run_through_module(SyllablesPhonotypes(['sro', 'zpa', 'dem'],
                                                      [[CONS, SONOR, VOWEL], [CONS, CONS, VOWEL], [CONS, VOWEL, SONOR]]))
        self.assertEqual(word.get_syllables(), ['sro', 'zpa', 'dem'])
        self.assertEqual(word.get_lengths(), [3, 3, 3])

    def test_vedomi(self):
        word = run_through_module(SyllablesPhonotypes(['vě', 'do', 'mí'], [[CONS, VOWEL], [CONS, VOWEL], [SONOR, VOWEL]]))
        self.assertEqual(word.get_syllables(), ['vě', 'do', 'mí'])
        self.assertEqual(word.get_lengths(), [3, 2, 2])

    def test_sex(self):
        word = run_through_module(SyllablesPhonotypes(['sex'], [[CONS, VOWEL, CONS]]))
        self.assertEqual(word.get_syllables(), ['sex'])
        self.assertEqual(word.get_lengths(), [4])

    def test_dě(self):
        word = run_through_module(SyllablesPhonotypes(['za', 'hra', 'dě'], [[CONS, VOWEL], [CONS, SONOR, VOWEL], [CONS, VOWEL]]))
        self.assertEqual(word.get_syllables(), ['za', 'hra', 'dě'])
        self.assertEqual(word.get_lengths(), [2, 3, 2])

    def test_ně(self):
        word = run_through_module(SyllablesPhonotypes(['ně'], [[SONOR, VOWEL]]))
        self.assertEqual(word.get_syllables(), ['ně'])
        self.assertEqual(word.get_lengths(), [2])


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


pin = Pipe(Queue(), Condition())
pout = Pipe(Queue(), Condition())
cd = ConfigData("conf_cs_lat.json")
mod = CountModule([pin, pout], cd, "blabla")

if __name__ == '__main__':
    unittest.main()




