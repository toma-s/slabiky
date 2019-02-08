from pipe import Pipe
from queue import Queue
from threading import Condition
from application.py_scripts.phonotype_module import PhonotypeModule
from application.py_scripts.word import Text, TextPhonotypes
from application.py_scripts.constants import SONOR, CONS, VOWEL, SPEC, SUBUNIT
from application.py_scripts.end import End
from application.py_scripts.config_data import ConfigData
from pathlib import Path
from application.py_scripts.init_terminate_module import InitTerminateModule
import unittest
import os

class FinalTests(unittest.TestCase):

    def __init__(self, parameter):
        super().__init__(parameter)
        self.encoding = 'UTF-8-sig'
        self.config_path = '../configs/'
        self.syllable_text_expected = ''
        self.syllable_text = ''
        self.syllable_lengths_expected = ''
        self.syllable_lengths = ''

    def test_czech(self):
        path = 'test_files/czech/'

        init = InitTerminateModule('test_czech.txt', path, self.encoding,
                                   self.config_path + 'conf_cs_lat.json')
        init.run()

        self.open_files(path)
        self.remove_temp_files(path)
        self.test()

    def test_belarussian(self):
        path = 'test_files/belarussian/'

        init = InitTerminateModule('test_belarussian.txt', path, self.encoding,
                                   self.config_path + 'conf_be_cyr.json')
        init.run()

        self.open_files(path)
        self.remove_temp_files(path)
        self.differences(path)
        self.test()

    def test_croatian(self):
        path = 'test_files/croatian/'

        init = InitTerminateModule('test_croatian.txt', path, self.encoding,
                                   self.config_path + 'conf_hr_lat.json')
        init.run()

        self.open_files(path)
        self.remove_temp_files(path)
        self.differences(path)
        self.test()

    def test_lower_sorbian(self):
        path = 'test_files/lower_sorbian/'

        init = InitTerminateModule('test_lower_sorbian.txt', path, self.encoding,
                                   self.config_path + 'conf_dsb_lat.json')
        init.run()

        self.open_files(path)
        self.remove_temp_files(path)
        self.differences(path)
        self.test()

    def test_macedonian(self):
        path = 'test_files/macedonian/'

        init = InitTerminateModule('test_macedonian.txt', path, self.encoding,
                                   self.config_path + 'conf_mk_cyr.json')
        init.run()

        self.open_files(path)
        # self.remove_temp_files(path)
        self.differences(path)
        self.test()

    def test_polish(self):
        path = 'test_files/polish/'

        init = InitTerminateModule('test_polish.txt', path, self.encoding,
                                   self.config_path + 'conf_pl_lat.json')
        init.run()

        self.open_files(path)
        self.remove_temp_files(path)
        self.differences(path)
        self.test()

    def test_russian(self):
        path = 'test_files/russian/'

        init = InitTerminateModule('test_russian.txt', path, self.encoding,
                                   self.config_path + 'conf_ru_cyr.json')
        init.run()

        self.open_files(path)
        self.remove_temp_files(path)
        self.test()

    def test_serbian(self):
        path = 'test_files/serbian/'

        init = InitTerminateModule('test_serbian.txt', path, self.encoding,
                                   self.config_path + 'conf_sr_cyr.json')
        init.run()

        self.open_files(path)
        self.remove_temp_files(path)
        # self.differences(path)
        self.test()

    def test_slovene(self):
        path = 'test_files/slovene/'

        init = InitTerminateModule('test_slovene.txt', path, self.encoding,
                                   self.config_path + 'conf_sl_lat.json')
        init.run()

        self.open_files(path)
        self.remove_temp_files(path)
        self.test()

    def test_ukrainian(self):
        path = 'test_files/ukrainian/'

        init = InitTerminateModule('test_ukrainian.txt', path, self.encoding,
                                   self.config_path + 'conf_uk_cyr.json')
        init.run()

        self.open_files(path)
        self.remove_temp_files(path)
        self.differences(path)
        self.test()

    def test_upper_sorbian(self):
        path = 'test_files/upper_sorbian/'

        init = InitTerminateModule('test_upper_sorbian.txt', path, self.encoding,
                                   self.config_path + 'conf_hsb_lat.json')
        init.run()

        self.open_files(path)
        self.remove_temp_files(path)
        self.differences(path)
        self.test()

    def remove_temp_files(self, path):
        os.remove(path + 'syllable_lengths_text.txt')
        os.remove(path + 'syllable_text.txt')
        os.remove(path + 'syllables_multiplicity.xls')
        os.remove(path + 'number_of_length_of_syllables_without_repetition.xls')
        os.remove(path + 'number_of_length_of_syllables_with_repetition.xls')

    def open_files(self, path):
        with open(path + 'syllable_lengths_text_expected.txt', encoding=self.encoding) as file:
            self.syllable_lengths_expected = file.read()
        file.close()

        with open(path + 'syllable_lengths_text.txt', encoding=self.encoding) as file:
            self.syllable_lengths = file.read()
        file.close()

        with open(path + 'syllable_text_expected.txt', encoding=self.encoding) as file:
            self.syllable_text_expected = file.read()
        file.close()

        with open(path + 'syllable_text.txt', encoding=self.encoding) as file:
            self.syllable_text = file.read()
        file.close()

    def test(self):
        self.assertEqual(self.syllable_text_expected, self.syllable_text)
        self.assertEqual(self.syllable_lengths_expected, self.syllable_lengths)

    def differences(self, path):
        if (self.syllable_text_expected != self.syllable_text
                or self.syllable_lengths_expected != self.syllable_lengths):
            ste = self.syllable_text_expected.split(' ')
            st = self.syllable_text.split(' ')
            sle = self.syllable_lengths_expected.split(' ')
            sl = self.syllable_lengths.split(' ')

            for i in range(len(ste)):
                a = ste[i]
                b = sle[i]
                c = st[i]
                d = sl[i]
                if (a != c or b != d):
                    print("Expected: " + a + " " + b)
                    print("Actual: " + c + " " + d)