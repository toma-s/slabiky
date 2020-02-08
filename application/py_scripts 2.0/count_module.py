from result_module import ResultModule
from thread_module import ThreadModule
from config_data import ConfigData
from word import SyllablesLengths
from end import End
from pipe import Pipe
from constants import *
import re

ERROR_LENGTH = -999
NO_INDEX = -99
NEXTS_DONT_EXIST = PREC_DONT_EXIST = (None,None)
svk_symbols_map = {'\$': 'ia', '&': 'ie', '%': 'iu', '§': 'ou', '#': 'au' }


class CountModule(ThreadModule):
    def __init__(self, pipes, data, file_path):
        super().__init__(pipes)
        self._data = data
        self._file_path = file_path
        self.lengths_of_syllables = {}
        self.frequencies_of_syllables = {}
        self.word = None
        self.index_of_syllable = NO_INDEX
        self.syllable_contains_special_symbol = False
        self.set_of_syllables_with_special_symbols = set()

    def run(self):
        pipe_in = self.get_pipes()[0]
        pipe_out = self.get_pipes()[1]
        self.running = True
        while self.running:
            self.handle_next_word(pipe_in, pipe_out)
        self.start_result_module()

    def start_result_module(self):
        self.replace_syllables_in_maps_if_needed()
        ResultModule(self.lengths_of_syllables, self.frequencies_of_syllables, self._file_path).run()

    def replace_syllables_in_maps_if_needed(self):
        if self._data.lang_name != "Slovak":
            return
        for syllable in self.set_of_syllables_with_special_symbols:
            length = self.lengths_of_syllables[syllable]
            frequency = self.frequencies_of_syllables[syllable]
            del self.lengths_of_syllables[syllable]
            del self.frequencies_of_syllables[syllable]
            replaced_syllable = self.replace_symbols_svk(syllable)
            self.lengths_of_syllables[replaced_syllable] = length
            self.frequencies_of_syllables[replaced_syllable] = frequency

    def handle_next_word(self, pipe_in, pipe_out):
        self.word = self.get_word(pipe_in)
        self.is_end()
        if self.running:
            output_word = self.process_all_syllables()
        else:
            output_word = self.word
        self.send_word(output_word, pipe_out)

    def get_word(self, pipe_in):
        pipe_in.acquire()
        if pipe_in.empty():
            pipe_in.wait()
        input_word = pipe_in.get()
        pipe_in.release()
        return input_word

    def is_end(self):
        if isinstance(self.word, End):
            self.running = False

    def send_word(self, word, pout):
        pout.acquire()
        pout.put(word)
        pout.notify()
        pout.release()

    def process_all_syllables(self):
        syllables_of_word = self.word.get_syllables()
        lengths_of_syllables_of_word = []
        for index_of_syllable in range(len(syllables_of_word)):
            self.syllable_contains_special_symbol = False
            self.index_of_syllable = index_of_syllable
            lengths_of_syllables_of_word.append(self.process_one_syllable())
            if self.syllable_contains_special_symbol:
                self.set_of_syllables_with_special_symbols.add(syllables_of_word[index_of_syllable])
                syllables_of_word[index_of_syllable] = self.replace_symbols_svk(syllables_of_word[index_of_syllable])
        return SyllablesLengths(syllables_of_word, lengths_of_syllables_of_word)

    def process_one_syllable(self):
        self.adjust_syllable_frequency(self.word.get_syllables()[self.index_of_syllable])
        return self.find_syllable_length()

    def find_syllable_length(self):
        syllable = self.word.get_syllables()[self.index_of_syllable]
        if self.lenght_of_syllable_is_unknown(syllable):
            self.lengths_of_syllables[syllable] = self.count_length_of_syllable()
        return self.lengths_of_syllables[syllable]

    def count_length_of_syllable(self):
        length = 0
        for index_of_letter in range(len(self.word.get_syllables()[self.index_of_syllable])):
            if self._data.lang_name == "Slovak" and self.is_special_symbol_svk(self.word.get_syllables()[index_of_letter]):
                self.syllable_contains_special_symbol = True
            if self.letter_already_counted(index_of_letter, self.word.get_phonotypes()[self.index_of_syllable]):
                continue
            length += self.find_length_of_letter(index_of_letter)
        return length

    def find_length_of_letter(self, index_of_letter):
        length_of_letter = self.find_length_value(index_of_letter)
        length_of_letter = self.check_special_length_cases(index_of_letter, length_of_letter)
        return length_of_letter

    def find_length_value(self, index_of_letter):
        syllable = self.word.get_syllables()[self.index_of_syllable]
        if self.is_subunit(self.word.get_phonotypes()[self.index_of_syllable], index_of_letter):
            length_of_letter = self.find_length_of_cluster(syllable[index_of_letter], syllable[index_of_letter + 1])
        else:
            length_of_letter = self.find_length_of_one_character_letter(index_of_letter, syllable)
        return length_of_letter

    def check_special_length_cases(self, index_of_letter, length_of_letter):
        if length_of_letter == -1:
            length_of_letter = self.check_special_sound_length(index_of_letter)
        return length_of_letter

    def find_length_of_one_character_letter(self, index_of_letter, syllable):
        return self._data.letter_to_phon_len[syllable[index_of_letter]]

    def find_length_of_cluster(self, letter, next_letter):
        return self._data.clusters[letter][next_letter]['length']

    def find_next_letter_and_phonotype_if_exist(self, index_of_letter):
        index_of_letter = self.get_end_of_letter_index(index_of_letter, self.index_of_syllable)
        if self.is_last_letter_of_word(self.word.get_syllables(), index_of_letter):
            return NEXTS_DONT_EXIST
        next_letter_syllable_index, next_index = self.get_position_of_next_letter(index_of_letter,
                                                                                  self.index_of_syllable)
        return self.find_next_letter_and_phonotype_with_index(next_letter_syllable_index, next_index)

    def get_end_of_letter_index(self, index_of_letter, index_of_syllable):
        if self.is_subunit(self.word.get_phonotypes()[index_of_syllable], index_of_letter):
            index_of_letter += 1
        return index_of_letter

    def get_position_of_next_letter(self, index_of_letter, syllable_index):
        next_index = index_of_letter + 1
        if self.is_last_letter_of_syllable(index_of_letter, self.word.get_syllables()[syllable_index]):
            next_index = 0
            syllable_index += 1
        return syllable_index, next_index

    def find_next_letter_and_phonotype_with_index(self, next_letter_syllable_index, next_letter_index):
        next_letter = self.word.get_syllables()[next_letter_syllable_index][next_letter_index]
        next_letter_index = self.get_end_of_letter_index(next_letter_index, next_letter_syllable_index)
        next_phonotype = self.word.get_phonotypes()[next_letter_syllable_index][next_letter_index]
        return next_letter, next_phonotype

    def find_preceding_letter_and_phonotype_if_exist(self, index_of_letter):
        if self.is_first_letter_of_word(index_of_letter):
            return PREC_DONT_EXIST
        last_letter_syllable_index, last_index = self.get_position_of_last_letter(index_of_letter,
                                                                                  self.index_of_syllable)
        return self.find_last_letter_and_phonotype_with_index(last_letter_syllable_index, last_index)

    def find_last_letter_and_phonotype_with_index(self, last_letter_syllable_index, last_letter_index):
        last_letter = self.word.get_syllables()[last_letter_syllable_index][last_letter_index]
        if self.is_spec(self.word.get_phonotypes()[last_letter_syllable_index], last_letter_index):
            last_letter_index -= 1
        last_phonotype = self.word.get_phonotypes()[last_letter_syllable_index][last_letter_index]
        return last_letter, last_phonotype

    def get_position_of_last_letter(self, index_of_letter, index_of_syllable):
        last_index = index_of_letter - 1
        if self.is_first_letter_of_syllable(index_of_letter):
            index_of_syllable -= 1
            last_index = -1
        return index_of_syllable, last_index

    def check_special_sound_length(self, index_of_letter):
        following_letter, following_phonotype = \
            self.find_next_letter_and_phonotype_if_exist(index_of_letter)
        preceding_letter, preceding_phonotype = \
            self.find_preceding_letter_and_phonotype_if_exist(index_of_letter)
        letter = self.get_whole_letter(index_of_letter)
        return self.find_lenght_fulfilling_condition(following_letter, following_phonotype, letter, preceding_letter,
                                                     preceding_phonotype)

    def find_lenght_fulfilling_condition(self, following_letter, following_phonotype,
                                         letter, preceding_letter, preceding_phonotype):
        for length in ("0", "1", "2"):
            for condition in self._data.spec_sound_len[letter][length]:
                if self.condition_fulfilled(condition, following_letter, following_phonotype,
                                            preceding_letter, preceding_phonotype):
                    return int(length)
        return ERROR_LENGTH

    def get_whole_letter(self, index_of_letter):
        letter = self.word.get_syllables()[self.index_of_syllable][index_of_letter]
        if self.is_subunit(self.word.get_phonotypes()[self.index_of_syllable], index_of_letter):
            letter += self.word.get_syllables()[self.index_of_syllable][index_of_letter + 1]
        return letter

    def lenght_of_syllable_is_unknown(self, syllable):
        return syllable not in self.lengths_of_syllables

    def adjust_syllable_frequency(self, syllable):
        self.frequencies_of_syllables[syllable] = self.frequencies_of_syllables.get(syllable, 0) + 1

    def letter_already_counted(self, index_of_letter, phonotypes_of_syllable):
        if index_of_letter == 0:
            return False
        return self.is_subunit(phonotypes_of_syllable, index_of_letter - 1) or \
               self.is_spec(phonotypes_of_syllable, index_of_letter)

    def is_subunit(self, syllable_phonotypes, index_of_letter):
        return syllable_phonotypes[index_of_letter] == SUBUNIT

    def is_spec(self, syllable_phonotypes, index_of_letter):
        syllable_phonotypes[index_of_letter] == SPEC

    def is_last_letter_of_word(self, word_syllables, index_of_letter):
        return self.index_of_syllable == len(word_syllables) - 1 and \
               index_of_letter == len(word_syllables[self.index_of_syllable])-1

    def is_last_letter_of_syllable(self, index_of_letter, syllable):
        return index_of_letter + 1 == len(syllable)

    def is_first_letter_of_word(self, index_of_letter):
        return self.index_of_syllable == 0 and index_of_letter == 0

    def is_first_letter_of_syllable(self, index_of_letter):
        return index_of_letter == 0

    def condition_fulfilled(self, condition, following_letter, following_phonotype,
                            preceding_letter, preceding_phonotype):
        return (following_letter in condition['following']['letters'] or
                following_phonotype in condition['following']['signs']) and \
               (preceding_letter in condition['preceding']['letters'] or
                preceding_phonotype in condition['preceding']['signs'])

    def is_special_symbol_svk(self, letter):
        return letter in ['$', '&', '%', '§', '#']

    def replace_symbols_svk(self, syllable):
        for key in svk_symbols_map:
            syllable = re.sub(key, svk_symbols_map[key], syllable)
        return syllable