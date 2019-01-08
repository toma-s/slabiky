import time

from end import End
from thread_module import ThreadModule
from word import TextPhonotypes


class PhonotypeModule(ThreadModule):
    def __init__(self, pipes, data):
        super().__init__(pipes)
        self._data = data

    def run(self):
        pipe_in = self.get_pipes()[0]
        pipe_out = self.get_pipes()[1]
        while True:
            pipe_in.acquire()
            if pipe_in.empty():
                print('Phonotype Module {}: No word yet, waiting'.format(self._thread.getName()))
                pipe_in.wait()
            word = pipe_in.get()
            pipe_in.release()

            if isinstance(word, End):
                print('Phonotype Module {}: Got to the End, sending'.format(self._thread.getName()))
                pipe_out.acquire()
                pipe_out.put(word)
                print('Phonotype Module {}: Finished working'.format(self._thread.getName()))
                break
            else:
                print('Phonotype Module {}: Got a word with text "{}", syllabifying'
                      .format(self._thread.getName(), '-'.join(word.get_text())))
                phono_word = self.set_phonotypes(word)
                if phono_word is None:
                    pass
                print('Phonotype Module {}: Set phonotypes to word with "{}", sending'
                      .format(self._thread.getName(), phono_word._text))
                pipe_out.acquire()
                pipe_out.put(phono_word)

            pipe_out.notify()
            pipe_out.release()
            time.sleep(1)

    def set_phonotypes(self, word) -> TextPhonotypes:
        # set phonotypes ...
        # ... got this gummy item:
        return TextPhonotypes(word.get_text()[:], ['phonotype', 'phonotype', 'phonotype', 'phonotype', 'phonotype'])
