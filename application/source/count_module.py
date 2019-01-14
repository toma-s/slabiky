import time

from application.source.end import End
from application.source.result_module import ResultModule
from application.source.thread_module import ThreadModule
from application.source.word import SyllablesLengths


class CountModule(ThreadModule):
    def __init__(self, pipes, data, file_path):
        super().__init__(pipes)
        self._data = data
        self._file_path = file_path

    def run(self):
        pipe_in = self.get_pipes()[0]
        pipe_out = self.get_pipes()[1]
        while True:
            pipe_in.acquire()
            if pipe_in.empty():
                print('Count Module {}: No word yet, waiting'.format(self._thread.getName()))
                pipe_in.wait()
            word = pipe_in.get()
            pipe_in.release()

            lens = ...
            freqs = ...

            if isinstance(word, End):
                print('Count Module {}: Got to the End, sending'.format(self._thread.getName()))
                pipe_out.acquire()
                pipe_out.put(word)
                print('Count Module {}: Calling Result Module'.format(self._thread.getName()))
                ResultModule(lens, freqs, self._file_path).run()
                print('Count Module {}: Finished working'.format(self._thread.getName()))
                break
            else:
                print('Count Module {}: Got a word with syllables "{}", counting'
                      .format(self._thread.getName(), word.get_syllables()))
                counted = self.count(word)
                counted_word = counted[0]
                lens.append(counted[1])
                lens.append(counted[2])
                print('Count Module {}: Counted word with syllables "{}", sending'
                      .format(self._thread.getName(), counted_word.get_syllables()))
                pipe_out.acquire()
                pipe_out.put(counted_word)

            pipe_out.notify()
            pipe_out.release()
            time.sleep(1)

    def count(self, word) -> tuple:
        # counted syllables lengths ...
        # ... got this gummy item:
        return (SyllablesLengths(word.get_syllables()[:], ['syll-length', 'syll-length']),
                ...,
                ...)



