from end import End
from pipe import Pipe
from thread_module import ThreadModule
from word import Text, TextPhonotypes
from constants import *


class PhonotypeModule(ThreadModule):
    def __init__(self, pipes, data):
        super().__init__(pipes)

        self.signs = data.letter_to_sign
        self.clusters = data.clusters
        self.cluster_letters = data.cluster_letters
        self.phono_changes = data.phono_changes
        self.text_changes = data.text_changes
        self.phonotypes = []
        self.running = False

    def run(self):
        pipe_in = self.get_pipes()[0]
        pipe_out = self.get_pipes()[1]
        self.running = True

        while self.running:
            self.handle_next_word(pipe_in, pipe_out)

    def handle_next_word(self, pin, pout):
        word = self.get_word(pin)
        self.is_end(word, pout)
        if self.running:
            word = self.set_phonotypes(word)
            if VOWEL in word.get_phonotypes() or word.get_text in data['one-syllable-words']:
                self.send_word(word, pout)

    def get_word(self, pin):
        pin.acquire()
        if pin.empty():
            pin.wait()
        word = pin.get()
        pin.release()
        return word

    def is_end(self, word, pout):
        if isinstance(word, End):
            self.send_word(word, pout)
            self.running = False

    def send_word(self, word, pout):
        pout.acquire()
        pout.put(word)
        pout.notify()
        pout.release()

    def text_changes_func(self, word):
        text_changes = self.text_changes

        for substr_to_change in text_changes:
            becomes = text_changes[substr_to_change]['becomes']
            word = word.replace(substr_to_change, becomes)

        return word

    def phonotype_changes_func(self, word_text, previous_letter, current_letter, next_letter):
        preceding_signs = self.phono_changes[current_letter]['preceding']['signs']
        preceding_letters = self.phono_changes[current_letter]['preceding']['letters']
        following_signs = self.phono_changes[current_letter]['following']['signs']
        following_letters = self.phono_changes[current_letter]['following']['letters']
        becomes = self.phono_changes[current_letter]['becomes']
        only_in_word = self.phono_changes[current_letter]['only_in_word']
        signs = self.signs

        is_exception = False

        def apply_phonotype_excption():
            self.phonotypes.append(becomes)
            return True

        def letter_exists(letter):
            if letter == "":
                return False
            return True

        previous_sign = signs[previous_letter] if previous_letter != "" else None
        next_sign = signs[next_letter] if next_letter != "" else None

        if word_text in only_in_word:
            is_exception = apply_phonotype_excption()

        elif letter_exists(next_letter) and letter_exists(previous_letter):
            if (previous_sign in preceding_signs or previous_letter in preceding_letters) \
                    and (next_sign in following_signs or next_letter in following_letters):
                is_exception = apply_phonotype_excption()

        elif not letter_exists(previous_letter) and None in preceding_signs:
            if next_sign in following_signs:
                is_exception = apply_phonotype_excption()

        elif not letter_exists(next_letter) and None in following_signs:
            if previous_sign in preceding_signs:
                is_exception = apply_phonotype_excption()

        return is_exception

    def clusters_func(self, word_text, current_letter, next_letter, exception_next_letter):
        except_in_subword = self.clusters[current_letter][next_letter + exception_next_letter]['except_in_subword']
        only_in_subword = self.clusters[current_letter][next_letter + exception_next_letter]['only_in_subword']
        except_in_subword_length = len(except_in_subword)
        only_in_subword_length = len(only_in_subword)
        phonotypes = self.phonotypes
        phonotype = self.clusters[current_letter][next_letter + exception_next_letter]["phonotype"]
        signs = self.signs

        is_exception = current_to_subunit_next_unchanged = False

        def apply_cluster_exeption():
            phonotypes.append(phonotype)
            return True

        if except_in_subword_length == 0 and only_in_subword_length == 0:
            if exception_next_letter != "":
                phonotypes.append(SUBUNIT)
            phonotypes.append(SUBUNIT)
            is_exception = apply_cluster_exeption()

        elif except_in_subword_length != 0:
            for subword in except_in_subword:
                if subword in word_text:
                    phonotypes.append(signs[current_letter])
                    is_exception = apply_cluster_exeption()

            if not is_exception:
                phonotypes.append(SUBUNIT)
                current_to_subunit_next_unchanged = True

        elif only_in_subword_length != 0:
            for word in only_in_subword:
                if word in word_text:
                    phonotypes.append(SUBUNIT)
                    is_exception = apply_cluster_exeption()

        return is_exception, current_to_subunit_next_unchanged

    def set_phonotypes(self, word) -> TextPhonotypes:
        cluster_letters = self.cluster_letters
        phono_changes = self.phono_changes
        signs = self.signs

        word_text = self.text_changes_func(word.get_text())  # TEXT CHANGES
        word_length = len(word_text)

        cluster_exception = False
        cluster_croatian_exception = False

        for i in range(word_length):

            if cluster_exception:
                cluster_exception = False
                continue

            if cluster_croatian_exception:
                cluster_croatian_exception = False
                continue

            current_to_subunit_next_unchanged = phonotype_exception = False

            previous_letter = word_text[i - 1] if i - 1 >= 0 else ""
            current_letter = word_text[i]
            next_letter = word_text[i + 1] if i + 1 < word_length else ""
            exception_next_letter = word_text[i + 2] if i + 2 < word_length else "" # used because of exception in croatian language (ije -> [SUBUNIT, SUBUNIT, VOWEL])

            if current_letter in cluster_letters:  # CLUSTERS

                if exception_next_letter != "" and next_letter + exception_next_letter in cluster_letters[current_letter]:
                    cluster_exception, current_to_subunit_next_unchanged = \
                        self.clusters_func(word_text, current_letter, next_letter, exception_next_letter)
                    cluster_croatian_exception = True

                if next_letter in cluster_letters[current_letter]:
                    cluster_exception, current_to_subunit_next_unchanged = \
                        self.clusters_func(word_text, current_letter, next_letter, "")

            elif current_letter in phono_changes:  # PHONOTYPE CHANGES
                phonotype_exception = self.phonotype_changes_func(word_text, previous_letter,
                                                                  current_letter, next_letter)

            no_exceptions = not current_to_subunit_next_unchanged and not cluster_exception and not phonotype_exception

            if no_exceptions:
                self.phonotypes.append(signs[current_letter])

        phonotypes = self.phonotypes
        self.phonotypes = []

        return TextPhonotypes(word_text, phonotypes)
