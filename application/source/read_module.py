import time

from end import End
from module import Module
from word import TextPunctuation


class ReadModule(Module):
    def __init__(self, pipes, file_path, encoding, data):
        super(Module).__init__()
        self._pipes = pipes
        self._file_path = file_path
        self._encoding = encoding
        self._data = data

    def run(self):
        pipe_out = self._pipes[0]

        print('Read Module: Started reading the input')
        words = self.read()
        print('Read Module: Finished reading the input')

        for word in words:
            pipe_out.acquire()
            if isinstance(word, End):
                print('Read Module: Sending the End')
            else:
                print('Read Module: Sending word with text "{}"'
                      .format(''.join(word.get_text())))
            pipe_out.put(word)
            pipe_out.notify()
            pipe_out.release()
            time.sleep(3)
        pipe_out.acquire()
        pipe_out.put(End())
        pipe_out.notify()
        pipe_out.release()

        print('Read Module: Finished working')

    def read(self) -> list:
        # with open (file_path, encoding) ...
        # ... got these gummy items:
        return [
            TextPunctuation(list('first'), [None, None, None, None, None]),
            TextPunctuation(list('second'), [None, None, None, None, None, None]),
            TextPunctuation(list('third'), [None, None, None, None, None])]
