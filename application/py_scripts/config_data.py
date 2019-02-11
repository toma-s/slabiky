import json
from constants import *


class ConfigData(object):
    def __init__(self, file_path):
        with open("" + file_path + "", encoding='utf-8') as config_file:
            data = json.load(config_file)

        """language"""
        # string
        self.lang_name = data['language']['name']

        # string
        self.lang_wr_sys = data['language']['writing_system']

        """lowercase"""
        # list
        self.letters = list(data['lowercase'].keys())

        # dict
        self.letter_to_phon_len = {letter: data['lowercase'][letter]['phoneme-length'] for letter in self.letters}

        # dict
        self.letter_to_sign = {letter: self.change_text_to_sign(data['lowercase'][letter]['sign']) for letter in
                               self.letters}

        # dict
        self.letter_to_subunit = {letter: data['lowercase'][letter]['subunit'] for letter in self.letters}

        """clusters"""
        # dict
        self.cluster_letters = {letter: list(data['clusters'][letter])
                                for letter in data['clusters'].keys()}

        # dict
        self.clusters = data['clusters']
        self.transform_clusters_phonotypes()

        """phonotype changes"""
        # dict
        self.phono_changes = data['phonotype_changes']
        self.transofrm_phono_changes_phonotypes()

        """text changes"""
        # dict
        self.text_changes = data['text_changes']

        """zero-syllable words"""
        # dict
        self.zero_syll_words = data['zero-syllable_words']

        """speial sound length"""
        # dict
        self.spec_sound_len = data['special_sound_length']
        self.transform_spec_sound_len_phonotypes()

    def change_text_to_sign(self, text):
        map = {"SONOR": SONOR, "CONS": CONS, "VOWEL": VOWEL, "SUBUNIT": SUBUNIT, "SPEC": SPEC, "NONE": None}
        return map.get(text, None)

    def transform_clusters_phonotypes(self):
        for first_letter in self.clusters:
            for second_letter in self.clusters[first_letter]:
                self.clusters[first_letter][second_letter]['phonotype'] = \
                    self.change_text_to_sign(self.clusters[first_letter][second_letter]['phonotype'])

    def transform_spec_sound_len_phonotypes(self):
        for letter in self.spec_sound_len:
            for length in ("0", "1", "2"):
                for condition in range(len(self.spec_sound_len[letter][length])):
                    for position in ("following", "preceding"):
                        self.spec_sound_len[letter][length][condition][position]['signs'] = \
                            self.change_array_of_texts_to_signs(
                                self.spec_sound_len[letter][length][condition][position]['signs'])

    def transofrm_phono_changes_phonotypes(self):
        for letter in self.phono_changes:
            self.phono_changes[letter]['preceding'] = self.change_array_of_texts_to_signs(
                self.phono_changes[letter]['preceding'])
            self.phono_changes[letter]['following'] = self.change_array_of_texts_to_signs(
                self.phono_changes[letter]['following'])
            self.phono_changes[letter]['becomes'] = self.change_text_to_sign(self.phono_changes[letter]['becomes'])

    def change_array_of_texts_to_signs(self, array):
        signs = []
        for phonotype in array:
            signs.append(self.change_text_to_sign(phonotype))
        return signs
