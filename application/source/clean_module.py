import time

from end import End
from thread_module import ThreadModule
from word import Text


class CleanModule(ThreadModule):
    def __init__(self, pipes, data):
        super().__init__(pipes)
        self._data = data

    def run(self):
        pipe_in = self.get_pipes()[0]
        pipe_out = self.get_pipes()[1]
        while True:
            pipe_in.acquire()
            if pipe_in.empty():
                print('Clean Module {}: No word yet, waiting'.format(self._thread.getName()))
                pipe_in.wait()
            word = pipe_in.get()
            pipe_in.release()

            if isinstance(word, End):
                print('Clean Module {}: Got to the End, sending'.format(self._thread.getName()))
                pipe_out.acquire()
                pipe_out.put(word)
                print('Clean Module {}: Finished working'.format(self._thread.getName()))
                break
            else:
                print('Clean Module {}: Got a word with text "{}", cleaning'
                      .format(self._thread.getName(), ''.join(word.get_text())))
                cleaned_word = self.clean(word)
                if cleaned_word is None:
                    pass
                print('Clean Module {}: Cleaned word with text "{}", sending'
                      .format(self._thread.getName(), cleaned_word._text))
                pipe_out.acquire()
                pipe_out.put(cleaned_word)

            pipe_out.notify()
            pipe_out.release()
            time.sleep(1)

    def clean(self, word) -> Text:
        # cleaned word ...
        # ... got this gummy item:
        return Text(word.get_text()[:])
