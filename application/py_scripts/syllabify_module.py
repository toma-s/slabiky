from end import End
from pipe import Pipe
from thread_module import ThreadModule
from word import SyllablesPhonotypes, TextPhonotypes
from constants import *

NO_PHONOTYPE_BREAKING_PRINCIPLE = -999


class SyllabifyModule(ThreadModule):
    running = False

    def __init__(self, pipes):
        super().__init__(pipes)

    def run(self):
        pipe_in = self.get_pipes()[0]
        pipe_out = self.get_pipes()[1]
        self.running = True

        while self.running:
            self.handle_next_word(pipe_in, pipe_out)

    def get_word(self, pipe_in):
        pipe_in.acquire()
        if pipe_in.empty():
            pipe_in.wait()
        word = pipe_in.get()
        pipe_in.release()
        return word

    def is_end(self, word):
        if isinstance(word, End):
            self.running = False

    def send_word(self, word, pout):
        pout.acquire()
        pout.put(word)
        pout.notify()
        pout.release()

    def syllabify(self, word) -> SyllablesPhonotypes:
        phonotypes = word.get_phonotypes()
        syllabified_phonotypes = self.syllabify_phonotypes(phonotypes)
        syllables = self.syllabify_text(word.get_text(), syllabified_phonotypes)
        return SyllablesPhonotypes(syllables, syllabified_phonotypes)

    def first_iteration_of_syllabification(self, phonotypes):
        partially_syllabified_phonotypes = self.split_after_each_vowel(phonotypes)
        if self.last_syllable_is_empty(partially_syllabified_phonotypes):
            return partially_syllabified_phonotypes[0:-1]
        return partially_syllabified_phonotypes

    def second_iteration_of_syllabification(self, syllabified_phonotypes):
        syllabified_phonotypes = self.check_sonority_principle(syllabified_phonotypes)
        if self.last_syllable_doesnt_contain_vowel(syllabified_phonotypes[-1]):
            syllabified_phonotypes = self.move_last_syllable_to_precedent(syllabified_phonotypes)
        return syllabified_phonotypes

    def syllabify_phonotypes(self, phonotypes):
        partially_syllabified_phonotypes = self.first_iteration_of_syllabification(phonotypes)
        return self.second_iteration_of_syllabification(partially_syllabified_phonotypes)

    def syllabify_text(self, text, syllabified_phonotypes):
        syllabified_text = []
        first_letter_of_syllable_index = 0
        for phonotype_syllable in syllabified_phonotypes:
            syllabified_text.append(self.get_syllable(text, first_letter_of_syllable_index, len(phonotype_syllable)))
            first_letter_of_syllable_index = self.next_syllable_starting_index(first_letter_of_syllable_index, len(phonotype_syllable))
        return syllabified_text

    def get_syllable(self, text, first_letter_of_syllable_index, length_of_syllable):
        return text[first_letter_of_syllable_index:first_letter_of_syllable_index + length_of_syllable]

    def next_syllable_starting_index(self, current_starting_index, length_of_current_syllable):
        return current_starting_index + length_of_current_syllable

    def handle_next_word(self, pipe_in, pipe_out):
        word = self.get_word(pipe_in)
        self.is_end(word)
        if self.running:
            word = self.syllabify(word)
        self.send_word(word, pipe_out)

    def split_after_each_vowel(self, phonotypes):
        partially_syllabified_phonotypes = [[]]
        for phonotype in phonotypes:
            partially_syllabified_phonotypes[-1].append(phonotype)
            if self.is_vowel(phonotype):
                partially_syllabified_phonotypes.append([])
        return partially_syllabified_phonotypes

    def last_syllable_is_empty(self, partially_syllabified_phonotypes):
        return partially_syllabified_phonotypes[-1] == []

    def check_sonority_principle(self, partially_syllabified_phonotypes):
        for i in range(1, len(partially_syllabified_phonotypes)):
            move_to_precedent_index = self.find_last_phonotype_in_syllable_breaking_principle(partially_syllabified_phonotypes[i])
            if self.letter_breaking_principle_exists(move_to_precedent_index):
                self.move_phonotypes_breaking_principle(move_to_precedent_index, partially_syllabified_phonotypes, i)
        return partially_syllabified_phonotypes

    def find_last_phonotype_in_syllable_breaking_principle(self, phonotype_syllable):
        move_to_precedent_index = NO_PHONOTYPE_BREAKING_PRINCIPLE
        for j in range(len(phonotype_syllable) - 1):
            next_index = self.find_index_of_next_phonotype(j, phonotype_syllable, len(phonotype_syllable) - 1)
            if self.breakes_sonority_principle(phonotype_syllable[j], phonotype_syllable[next_index], j, move_to_precedent_index):
                move_to_precedent_index = j
        return move_to_precedent_index

    def find_index_of_next_phonotype(self, j, phonotype_syllable, last_index):
        next_index = j + 1
        if phonotype_syllable[next_index] in [SPEC, SUBUNIT] and next_index != last_index:
            next_index += 1
        return next_index

    def breakes_sonority_principle(self, phonotype, next_phonotype, phonotype_index, last_index_breaking_principle):
        return (phonotype not in [SUBUNIT, SPEC] and  phonotype > next_phonotype) \
               or (phonotype_index == 0 and phonotype == SPEC) or (phonotype == SPEC and phonotype_index == last_index_breaking_principle+1);

    def move_phonotypes_breaking_principle(self, move_to_precedent_index, partially_syllabified_phonotypes, syllable_index):
        partially_syllabified_phonotypes[syllable_index - 1].extend(
            partially_syllabified_phonotypes[syllable_index][:move_to_precedent_index + 1])
        del partially_syllabified_phonotypes[syllable_index][:move_to_precedent_index + 1]
        return partially_syllabified_phonotypes

    def last_syllable_doesnt_contain_vowel(self, syllable):
        return VOWEL not in syllable

    def move_last_syllable_to_precedent(self, syllabified_phonotypes):
        syllabified_phonotypes[-2].extend(syllabified_phonotypes[-1])
        syllabified_phonotypes = syllabified_phonotypes[0:-1]
        return syllabified_phonotypes

    def is_vowel(self, phonotype):
        return phonotype == VOWEL

    def letter_breaking_principle_exists(self, index):
        return index != NO_PHONOTYPE_BREAKING_PRINCIPLE
