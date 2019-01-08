from end import End
from thread_module import ThreadModule


class WriteModule(ThreadModule):
    def __init__(self, pipes, file_path):
        super().__init__(pipes)
        self._file_path = file_path

    def run(self):
        pipe_in = self.get_pipes()[0]
        while True:
            pipe_in.acquire()
            if pipe_in.empty():
                print('Write Module {}: No word yet, waiting'.format(self._thread.getName()))
                pipe_in.wait()
            word = pipe_in.get()
            pipe_in.release()

            if isinstance(word, End):
                print('Write Module {}: Got to the End, finished working'.format(self._thread.getName()))
                break
            else:
                print('Write Module {}: Got a word with syllables "{}", writing'
                      .format(self._thread.getName(), word.get_syllables()))
                self.write_to_file()

    def write_to_file(self):
        pass
