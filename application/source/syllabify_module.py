import time

from application.source.end import End
from application.source.thread_module import ThreadModule
from application.source.word import SyllablesPhonotypes


class SyllabifyModule(ThreadModule):
    def __init__(self, pipes):
        super().__init__(pipes)

    def run(self):
        pipe_in = self.get_pipes()[0]
        pipe_out = self.get_pipes()[1]
        while True:
            pipe_in.acquire()
            if pipe_in.empty():
                print('Syllabify Module {}: No word yet, waiting'.format(self._thread.getName()))
                pipe_in.wait()
            word = pipe_in.get()
            pipe_in.release()

            if isinstance(word, End):
                print('Syllabify Module {}: Got to the End, sending'.format(self._thread.getName()))
                pipe_out.acquire()
                pipe_out.put(word)
                print('Syllabify Module {}: Finished working'.format(self._thread.getName()))
                break
            else:
                print('Syllabify Module {}: Got a word with text "{}", syllabifying'
                      .format(self._thread.getName(), '-'.join(word.get_text())))
                sylled_word = self.syllabify(word)
                if sylled_word is None:
                    pass
                print('Syllabify Module {}: Syllabified word with syllables "{}", sending'
                      .format(self._thread.getName(), sylled_word._syllables))
                pipe_out.acquire()
                pipe_out.put(sylled_word)

            pipe_out.notify()
            pipe_out.release()
            time.sleep(1)

    def syllabify(self, word) -> SyllablesPhonotypes:
        # cleaned word, set phonotypes ...
        # ... got this gummy item:
        syllables = [word.get_text()[:][:2], word.get_text()[:][2:]]
        return SyllablesPhonotypes(syllables, ['syll-phonotype', 'syll-phonotype'])
