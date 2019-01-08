import json


class ConfigData(object):
    def __init__(self, file_path):
        data = json.load(open(file_path, encoding='utf-8'))

        """language"""
        # string
        self.lang_name = data['language'][0]['name']

        # string
        self.lang_wr_sys = data['language'][0]['writing_system']

        """lowercase"""
        # list
        self.letters = list(data['lowercase'][0].keys())

        # dict
        self.letter_to_phon_len = ...

        # dict
        self.letter_to_sign = ...

        # dict
        self.letter_to_subunit = ...

        """clusters"""
        # dict
        self.cluster_letters = ...

        # dict
        self.clusters = ...

        """phonotype changes"""
        # dict
        self.phono_changes = ...

        """text changes"""
        # dict
        self.texts_changes = ...

        """zero-syllable words"""
        # dict
        self.zero_syll_words = ...

        """speial sound length"""
        # dict
        self.spec_sound_len = ...
