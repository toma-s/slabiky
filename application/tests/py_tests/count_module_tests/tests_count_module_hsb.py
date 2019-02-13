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

    def test_wrobl(self):
        word = run_through_module(SyllablesPhonotypes(['wro', 'bl'], [[SONOR, SONOR, VOWEL], [CONS, VOWEL]]))
        self.assertEqual(word.get_syllables(), ['wro', 'bl'])
        self.assertEqual(word.get_lengths(), [3, 2])

    def test_sneh(self):
        word = run_through_module(SyllablesPhonotypes(['sněh'], [[CONS, SONOR, VOWEL, CONS]]))
        self.assertEqual(word.get_syllables(), ['sněh'])
        self.assertEqual(word.get_lengths(), [3])

    def test_sahac(self):
        word = run_through_module(SyllablesPhonotypes(['sa', 'hać'], [[CONS, VOWEL,], [CONS, VOWEL, CONS]]))
        self.assertEqual(word.get_syllables(), ['sa', 'hać'])
        self.assertEqual(word.get_lengths(), [2, 3])

    def test_zwjetšeho(self):
        word = run_through_module(SyllablesPhonotypes(['zwje', 'tše', 'ho'], [[0, 4, 1, 2],[0, 0, 2], [0, 2]]))
        self.assertEqual(word.get_syllables(), ['zwje', 'tše', 'ho'])
        self.assertEqual(word.get_lengths(), [3, 3, 2])

    def test_zhorjelc(self):
        word = run_through_module(SyllablesPhonotypes(['zho', 'rjelc'], [[0, 0, 2], [4, 1, 2, 1, 0]]))
        self.assertEqual(word.get_syllables(), ['zho', 'rjelc'])
        self.assertEqual(word.get_lengths(), [2, 4])

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
cd = ConfigData("conf_hsb_lat.json")
mod = CountModule([pin, pout], cd, "blabla")

if __name__ == '__main__':
    unittest.main()




