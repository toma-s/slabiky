from config_data import ConfigData
from pipe import Pipe
from queue import Queue
from threading import Condition
from count_module import CountModule
from syllabify_module import SyllabifyModule
from word import TextPhonotypes, SyllablesLengths
from constants import SONOR, CONS, VOWEL, SPEC, SUBUNIT
from end import End
import unittest
import time

words_to_do = [
    TextPhonotypes('farmaceutický', [CONS, VOWEL, SONOR, SONOR, VOWEL, CONS,
                                     SUBUNIT, VOWEL, CONS, VOWEL, CONS, CONS, VOWEL]),
    TextPhonotypes('pouze', [CONS, SUBUNIT, VOWEL, CONS, VOWEL]),
    TextPhonotypes('použil', [CONS, VOWEL, VOWEL, CONS, VOWEL, SONOR]),
    TextPhonotypes('neurčitý', [SONOR, VOWEL, VOWEL, SONOR, CONS, VOWEL, CONS, VOWEL]),
    TextPhonotypes('automatický', [SUBUNIT, VOWEL, CONS, VOWEL, SONOR, VOWEL, CONS, VOWEL, CONS, CONS, VOWEL]),
    TextPhonotypes('vlna', [CONS, VOWEL, SONOR, VOWEL]),
    TextPhonotypes('osm', [VOWEL, CONS, VOWEL]),
    TextPhonotypes('bijologije', [CONS, VOWEL, SONOR, VOWEL, SONOR, VOWEL, CONS, VOWEL, SONOR, VOWEL]),
    TextPhonotypes('srozpadem', [CONS, SONOR, VOWEL, CONS, CONS, VOWEL, CONS, VOWEL, SONOR]),
    TextPhonotypes('vědomí', [CONS, VOWEL, CONS, VOWEL, SONOR, VOWEL]),
    TextPhonotypes('sex', [CONS, VOWEL, CONS])
        ]

syllables = [['fa', 'rma', 'ceu', 'ti', 'cký'], ['pou', 'ze'], ['po', 'u', 'žil'], ['ne', 'ur', 'či', 'tý'],
             ['au', 'to', 'ma', 'ti', 'cký'], ['vl', 'na'], ['o', 'sm'], ['bi', 'jo', 'lo', 'gi', 'je'],
             ['sro', 'zpa', 'dem'], ['vě', 'do', 'mí'], ['sex']]

lengths = [[2, 3, 2, 2, 3], [2, 2], [2, 1, 3], [2, 2, 2, 2],
           [1, 2, 2, 2, 3], [2, 2], [1, 2], [2, 2, 2, 2, 2],
           [3, 3, 3], [3, 2, 2], [4]]

lengths_map = {'au': 1, 'bi': 2, 'ceu': 2, 'cký': 3, 'dem': 3, 'do': 2, 'fa': 2, 'gi': 2, 'je': 2, 'jo': 2,
               'lo': 2, 'ma': 2, 'mí': 2, 'na': 2, 'ne': 2, 'o': 1, 'po': 2, 'pou': 2, 'rma': 3, 'sex': 4,
               'sm': 2, 'sro': 3, 'ti': 2, 'to': 2, 'tý': 2, 'u': 1, 'ur': 2, 'vl': 2, 'vě': 3, 'ze': 2,
               'či': 2, 'zpa': 3, 'žil': 3}

frequency_map = {'au': 1, 'bi': 1, 'ceu': 1, 'cký': 2, 'dem': 1, 'do': 1, 'fa': 1, 'gi': 1, 'je': 1, 'jo': 1,
                 'lo': 1, 'ma': 1, 'mí': 1, 'na': 1, 'ne': 1, 'o': 1, 'po': 1, 'pou': 1, 'rma': 1, 'sex': 1,
                 'sm': 1, 'sro': 1, 'ti': 2, 'to': 1, 'tý': 1, 'u': 1, 'ur': 1, 'vl': 1, 'vě': 1, 'ze': 1,
                 'či': 1, 'zpa': 1, 'žil': 1}

class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mod_syll.start()
        mod_count.start()

    @classmethod
    def tearDownClass(cls):
        run_through_module(End(), mod_syll)

    def test_cs(self):
        for word in words_to_do:
            run_through_module(word, mod_syll)
        time.sleep(1)
        index = 0
        while not pout.empty():
            word = pout.get()
            self.assertEqual(word.get_syllables(), syllables[index])
            self.assertEqual(word.get_lengths(), lengths[index])
            index += 1
        self.assertEqual(mod_count.lengths_of_syllables, lengths_map)
        self.assertEqual(mod_count.frequencies_of_syllables, frequency_map)


def run_through_module(word, mod):
    pin = mod.get_pipes()[0]
    pin.acquire()
    pin.put(word)
    pin.notify()
    pin.release()


pin = Pipe(Queue(), Condition())
pipe_syllabify_count = Pipe(Queue(), Condition())
pout = Pipe(Queue(), Condition())
cd = ConfigData("conf_cs_lat.json")
mod_syll = SyllabifyModule([pin, pipe_syllabify_count])
mod_count = CountModule([pipe_syllabify_count, pout], cd, "blabla")

if __name__ == '__main__':
    unittest.main()




