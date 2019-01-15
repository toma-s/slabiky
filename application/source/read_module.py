import time

from application.source import constants
from application.source.end import End
from application.source.word import TextPunctuation
from application.source.module import Module


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
                print('Read Module: Sending word with text "{}"'.format(''.join(word.get_text())))
            pipe_out.put(word)
            pipe_out.notify()
            pipe_out.release()

        pipe_out.acquire()
        pipe_out.put(End())
        pipe_out.notify()
        pipe_out.release()

        print('Read Module: Finished working')

    def read(self) -> list:

        words = []
        buffer_text = []
        buffer_signs = []
        dash = [False]

        with open(self._file_path, encoding=self._encoding) as input:
            while True:
                sym = input.read(1)
                if not sym:
                    if len(buffer_text):
                        word = TextPunctuation(''.join(buffer_text), buffer_signs)
                        words.append(word)
                    words.append(End())
                    break
                if sym in [' ', '\n', '\t', '\r']:
                    if len(buffer_text):
                        if dash[0] and sym != ' ':
                            buffer_signs[-1] = constants.HYPHEN
                            continue
                        word = TextPunctuation(''.join(buffer_text), buffer_signs)
                        words.append(word)
                    buffer_text = []
                    buffer_signs = []
                else:
                    dash[0] = False
                    to_text, to_signs = to_buffer(sym, dash)
                    buffer_text.extend(to_text)
                    buffer_signs.extend(to_signs)

        return words


def to_buffer(sym, dash) -> tuple:
    to_text, to_signs = [], []
    if sym in ['-']:
        to_text.append(sym)
        to_signs.append(constants.PUNCT)
        dash[0] = True
        return to_text, to_signs
    if sym in ['.', ',', ':', ';', '?', '!', '[', ']', '(', ')', '{', '}', '⟨', '⟩',
               '—', '―', '‹', '›', '«', '»', '“', '”', '"', '"', '‚', '‘']:
        to_text.append(sym)
        to_signs.append(constants.PUNCT)
        return to_text, to_signs
    to_text.append(sym)
    to_signs.append(None)

    return to_text, to_signs
