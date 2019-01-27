from application.source import constants
from application.source.end import End
from application.source.thread_module import ThreadModule
from application.source.word import Text, TextPunctuation

hyphen_dashes = ['-', '—', '―']
dashes = ['—', '―']
punctuation_to_erase = ['.', ',', ':', ';', '?', '!', '[', ']', '(', ')', '{', '}', '⟨', '⟩', '‹', '›', '«', '»',
                        '“', '”', '"', '"', '‚', '‘', '"', '„']


class CleanModule(ThreadModule):

    is_running = False

    def __init__(self, pipes, data):
        super().__init__(pipes)
        self._data = data

    def get_data(self):
        return self._data

    def run(self):
        pipe_in = self.get_pipes()[0]
        pipe_out = self.get_pipes()[1]
        self.is_running = True
        curr, foll = None, None

        while self.is_running:
            curr, foll = foll, get_word(pipe_in)
            self.is_end(foll)
            if not curr:
                continue

            print('Clean Module: Cleaning a word with text "{}"'.format(curr.get_text()))
            cleaned_words = self.clean([curr, foll])
            curr, foll = cleaned_words[0], cleaned_words[1]
            if not curr:
                print('Clean Module: Ignored the word')
                continue
            print('Clean Module: Cleaned word with text "{}"'.format(curr.get_text()))

            send_word(Text(curr.get_text()), pipe_out)

        print('Clean Module: Got to the End, sending End')
        send_word(foll, pipe_out)
        print('Clean Module: Finished')

    def is_end(self, word):
        if isinstance(word, End):
            self.is_running = False

    def clean(self, words: list) -> list:

        curr, foll = words[0], words[1]
        buffer_text, buffer_signs = [], []

        if len(curr.get_text()) != 1 and curr.get_text().isupper():
            return [None, foll]

        for i in range(len(curr.get_text())):
            sym = curr.get_text()[i]
            sign = curr.get_punctuation()[i]

            if sym == '.' and isinstance(foll, TextPunctuation) and not foll.get_text().istitle():
                return [None, foll]

            if not len(buffer_text) and sign == constants.PUNCT:
                if sym in punctuation_to_erase:
                    continue
                elif sym in dashes:
                    return [None, foll]

            if sign == constants.HYPHEN:
                if len(curr.get_text()) == i + 1:
                    return [None, foll]
                else:
                    continue

            if sign == constants.PUNCT and sym not in hyphen_dashes:
                for j in range(i + 1, len(curr.get_text())):
                    next_sign = curr.get_punctuation()[j]
                    if next_sign != constants.PUNCT:
                        return [None, foll]
                return [TextPunctuation(''.join(buffer_text), buffer_signs), foll]

            sym_low = sym.lower()
            if sym_low not in self.get_data().letters:
                return [None, foll]

            buffer_text.append(sym_low)
            buffer_signs.append(sign)

        curr = TextPunctuation(''.join(buffer_text), buffer_signs)

        if isinstance(foll, TextPunctuation) and len(foll.get_text()) == 1:
            foll_low = TextPunctuation(foll.get_text().lower(), foll.get_punctuation())
            if self.is_zero_syll(foll_low.get_text()):
                buffer_attach = self.get_attachment(foll_low)
                if buffer_attach['attachment'] == 'to_preceding':
                    buffer_text.append(foll_low.get_text())
                    buffer_signs.append(foll_low.get_punctuation())
                    foll = None
        elif len(curr.get_text()) == 1 and self.is_zero_syll(curr.get_text()):
            buffer_attach = self.get_attachment(curr)
            if buffer_attach['attachment'] == 'to_following':
                foll.set_text(curr.get_text() + foll.get_text())
                foll.set_punctuation(curr.get_punctuation() + foll.get_punctuation())
                return [None, foll]

        return [TextPunctuation(''.join(buffer_text), buffer_signs), foll]

    def is_zero_syll(self, text: str) -> bool:
        word = text[0]
        if word in self.get_data().zero_syll_words.keys():
            return True

    def get_attachment(self, word: TextPunctuation) -> dict:
        text = word.get_text()
        sign = word.get_punctuation()
        buffer_attach = dict()
        attachment = self.get_data().zero_syll_words[text]
        buffer_attach['attachment'] = attachment
        buffer_attach['text'] = text
        buffer_attach['sign'] = sign
        return buffer_attach


def send_word(word, pipe_out):
    pipe_out.acquire()
    pipe_out.put(word)
    pipe_out.notify()
    pipe_out.release()


def get_word(pipe_in):
    pipe_in.acquire()
    if pipe_in.empty():
        print('Clean Module: No word yet, waiting\n')
        pipe_in.wait()
    word = pipe_in.get()
    pipe_in.release()
    return word
