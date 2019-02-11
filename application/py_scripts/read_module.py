import constants
from end import End
from word import TextPunctuation
from module import Module

punctuation = ['-', '—', '―', '.', ',', ':', ';', '?', '!', '[', ']', '(', ')', '{', '}', '⟨', '⟩', '‹', '›', '«', '»',
               '“', '”', '"', '"', '‚', '‘', '"', '„']
spaces = [' ', '\n', '\t', '\r']


class ReadModule(Module):

    def __init__(self, pipes, file_path, encoding, data):
        super(Module).__init__()
        self._pipes = pipes
        self._file_path = file_path
        self._encoding = encoding
        self._data = data

    def run(self):
        pipe_out = self._pipes[0]

        words = self.read()

        for word in words:
            send_word(word, pipe_out)

        send_word(End(), pipe_out)

    def read(self) -> list:

        words = []
        buffer_text = []
        buffer_signs = []
        dash = [False]
        start = False

        with open(self._file_path, encoding=self._encoding) as input:
            while True:
                sym = input.read(1)
                if not sym:
                    if len(buffer_text):
                        word = TextPunctuation(''.join(buffer_text), buffer_signs)
                        words.append(word)
                    break
                if sym in spaces:
                    if not start:
                        continue
                    if len(buffer_text):
                        if dash[0] and sym != ' ':
                            buffer_signs[-1] = constants.HYPHEN
                            continue
                        word = TextPunctuation(''.join(buffer_text), buffer_signs)
                        words.append(word)
                    buffer_text = []
                    buffer_signs = []
                else:
                    start = True
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
    if sym in punctuation:
        to_text.append(sym)
        to_signs.append(constants.PUNCT)
        return to_text, to_signs
    to_text.append(sym)
    to_signs.append(None)

    return to_text, to_signs


def send_word(word, pipe_out):
    pipe_out.acquire()
    pipe_out.put(word)
    pipe_out.notify()
    pipe_out.release()
