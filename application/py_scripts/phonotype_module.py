import time

from end import End
from pipe import Pipe
from thread_module import ThreadModule
from word import Text, TextPhonotypes
from constants import *


class PhonotypeModule(ThreadModule):
    def __init__(self, pipes, data):
        super().__init__(pipes)

        self.signs           = data.letter_to_sign
        self.clusters        = data.clusters
        self.cluster_letters = data.cluster_letters
        self.phono_changes   = data.phono_changes
        self.text_changes    = data.text_changes
        self.phonotypes      = []

    def run(self):
        pipe_in = self.get_pipes()[0]
        pipe_out = self.get_pipes()[1]
        while True:
            pipe_in.acquire()
            if pipe_in.empty():
                pipe_in.wait()
            word = pipe_in.get()
            if (isinstance(word, End)):
                pipe_out.acquire()
                pipe_out.put(word)
                pipe_out.notify()
                pipe_out.release()
                break
            pipe_in.release()

            if isinstance(word, End):
                pipe_out.acquire()
                pipe_out.put(word)
                pipe_out.notify()
                pipe_out.release()
                break
            else:
                phono_word = self.set_phonotypes(word)
                if phono_word is None:
                    pass
                if (VOWEL in phono_word.get_phonotypes()):
                    pipe_out.acquire()
                    pipe_out.put(phono_word)
                    pipe_out.notify()
                    pipe_out.release()
                else:
                    pass

    def text_changes_func(self, word):
        text_changes = self.text_changes

        for substr_to_change in text_changes:
            becomes   = text_changes[substr_to_change]['becomes']
            word      = word.replace(substr_to_change, becomes)

        return word

    def phonotype_changes_func(self, word_text, previous_sign, current_sign, next_sign):
        only_in_word = self.phono_changes[current_sign]['only_in_word']
        preceding    = self.phono_changes[current_sign]['preceding']
        following    = self.phono_changes[current_sign]['following']
        becomes      = self.phono_changes[current_sign]['becomes']
        signs        = self.signs

        is_exception = False

        def apply_phonotype_excption():
            self.phonotypes.append(becomes)
            return True

        def sign_exists(sign):
            if sign is None:
                return False
            return True

        if word_text in only_in_word:
            is_exception = apply_phonotype_excption()

        elif sign_exists(next_sign) and sign_exists(previous_sign):
            if signs[previous_sign] in preceding and signs[next_sign] in following:
                is_exception = apply_phonotype_excption()

        elif not sign_exists(previous_sign) and None in preceding:
            if signs[next_sign] in following:
                is_exception = apply_phonotype_excption()

        elif not sign_exists(next_sign) and None in following:
            if signs[previous_sign] in preceding:
                is_exception = apply_phonotype_excption()

        return is_exception

    def clusters_func(self, word_text, current_sign, next_sign):
        except_in_subword        = self.clusters[current_sign][next_sign]['except_in_subword']
        only_in_subword          = self.clusters[current_sign][next_sign]['only_in_subword']
        except_in_subword_length = len(except_in_subword)
        only_in_subword_length   = len(only_in_subword)
        phonotypes               = self.phonotypes
        phonotype                = self.clusters[current_sign][next_sign]["phonotype"]
        signs                    = self.signs

        is_exception = current_to_subunit_next_unchanged = False

        def apply_cluster_excption():
            phonotypes.append(phonotype)
            return True

        if except_in_subword_length == 0 and only_in_subword_length == 0:
            phonotypes.append(SUBUNIT)
            is_exception = apply_cluster_excption()

        elif except_in_subword_length != 0:
            for subword in except_in_subword:
                if subword in word_text:
                    phonotypes.append(signs[current_sign])
                    is_exception = apply_cluster_excption()

            if not is_exception:
                phonotypes.append(SUBUNIT)
                current_to_subunit_next_unchanged = True

        elif only_in_subword_length != 0:
            for word in only_in_subword:
                if word in word_text:
                    phonotypes.append(SUBUNIT)
                    is_exception = apply_cluster_excption()

        return is_exception, current_to_subunit_next_unchanged

    def set_phonotypes(self, word) -> TextPhonotypes:
        cluster_letters = self.cluster_letters
        phono_changes   = self.phono_changes
        signs           = self.signs

        word_text   = self.text_changes_func(word.get_text()) # TEXT CHANGES
        word_length = len(word_text)

        cluster_exception = False

        for i in range(word_length):

            if cluster_exception:
                cluster_exception = False
                continue

            current_to_subunit_next_unchanged = phonotype_exception = False

            previous_sign = word_text[i - 1] if i - 1 >= 0 else None
            current_sign  = word_text[i]
            next_sign     = word_text[i + 1] if i + 1 < word_length else None

            if current_sign in cluster_letters and next_sign in cluster_letters[current_sign]: # CLUSTERS
                cluster_exception, current_to_subunit_next_unchanged = \
                    self.clusters_func(word_text, current_sign, next_sign)

            elif current_sign in phono_changes: # PHONOTYPE CHANGES
                phonotype_exception = self.phonotype_changes_func(word_text, previous_sign, current_sign, next_sign)

            no_exceptions = not current_to_subunit_next_unchanged and not cluster_exception and not phonotype_exception

            if no_exceptions:
                self.phonotypes.append(signs[current_sign])

        phonotypes = self.phonotypes
        self.phonotypes = []

        return TextPhonotypes(word_text, phonotypes)
