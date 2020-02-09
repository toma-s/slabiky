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

    def test_rz(self):
        word = run_through_module(SyllablesPhonotypes(['rž'], [[VOWEL, CONS]]))
        self.assertEqual(word.get_syllables(), ['rž'])
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
cd = ConfigData("../../configs/conf_sl_lat.json")
mod = CountModule([pin, pout], cd, "blabla")

if __name__ == '__main__':
    unittest.main()




