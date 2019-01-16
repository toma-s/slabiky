from application.source import constants
from application.source.end import End
from application.source.thread_module import ThreadModule
from application.source.word import Text, TextPunctuation


class CleanModule(ThreadModule):

    running = False

    def __init__(self, pipes, data):
        super().__init__(pipes)
        self._data = data

    def get_data(self):
        return self._data

    def run(self):
        pipe_in = self.get_pipes()[0]
        pipe_out = self.get_pipes()[1]
        self.running = True

        prec, curr, foll = None, None, None

        while self.running:
            pipe_in.acquire()
            if pipe_in.empty():
                print('Clean Module: No word yet, waiting')
                pipe_in.wait()
            prec, curr = curr, foll
            foll = pipe_in.get()
            pipe_in.release()

            if not curr:
                if isinstance(foll, End):
                    print('Clean Module: Got to the End, sending')
                    pipe_out.acquire()
                    pipe_out.put(foll)
                    pipe_out.notify()
                    pipe_out.release()
                    print('Clean Module: Finished working')
                    self.running = False

                if isinstance(foll, TextPunctuation):
                    print('Clean Module: Got a word with text "{}", waiting for the next one'
                          .format(''.join(foll.get_text())))
                    continue

            print('Clean Module: Cleaning a word with text "{}"'.format(''.join(curr.get_text())))

            cleaned_words = self.clean([prec, curr, foll])
            curr, foll = cleaned_words[1], cleaned_words[2]

            if curr:
                print('Clean Module: Cleaned word with text "{}", sending'.format(curr.get_text()))
                pipe_out.acquire()
                pipe_out.put(Text(curr.get_text()))
                pipe_out.notify()
                pipe_out.release()

            if isinstance(foll, End):
                print('Clean Module: Got to the End, sending')
                pipe_out.acquire()
                pipe_out.put(foll)
                pipe_out.notify()
                pipe_out.release()
                print('Clean Module: Finished working')
                self.running = False

    def clean(self, words: list) -> list:

        prec, curr, foll = words[0], words[1], words[2]
        buffer_text, buffer_signs = [], []
        punctuation_to_erase = ['.', ',', ':', ';', '?', '!', '[', ']', '(', ')', '{', '}',
                                '⟨', '⟩', '‹', '›', '«', '»', '“', '”', '"', '"', '‚', '‘', '"']
        dashes = ['-', '—', '―']

        for i in range(len(curr.get_text())):
            sym = curr.get_text()[i]
            sign = curr.get_punctuation()[i]

            if not len(buffer_text) and sign == constants.PUNCT:
                if sym in punctuation_to_erase:
                    continue
                elif sym in ['—', '―']:
                    return [prec, None, foll]

            if sign == constants.HYPHEN:
                try:
                    next_sym = curr.get_text()[i + 1]
                    continue
                except IndexError:
                    return [prec, None, foll]

            if sign == constants.PUNCT and sym not in dashes:
                for j in range(i + 1, len(curr.get_text())):
                    next_sign = curr.get_punctuation()[j]
                    if next_sign != constants.PUNCT:
                        return [prec, None, foll]
                return [prec, TextPunctuation(''.join(buffer_text), buffer_signs), foll]

            sym_low = sym.lower()
            if sym_low not in self.get_data().letters:
                return [prec, None, foll]

            buffer_text.append(sym_low)
            buffer_signs.append(sign)

        if isinstance(foll, TextPunctuation) and len(foll.get_text()) == 1 and self.is_zero_syll(foll.get_text()):
            buffer_attach = self.get_attachment(foll)
            if buffer_attach['attachment'] == 'to_preceding':
                buffer_text.append(foll.get_text())
                buffer_signs.append(foll.get_punctuation())
                foll = None
        elif isinstance(curr, TextPunctuation) and len(curr.get_text()) == 1 and self.is_zero_syll(curr.get_text()):
            buffer_attach = self.get_attachment(curr)
            if buffer_attach['attachment'] == 'to_following':
                foll.set_text(curr.get_text() + foll.get_text())
                foll.set_punctuation(curr.get_punctuation() + foll.get_punctuation())
                return [prec, None, foll]

        return [prec, TextPunctuation(''.join(buffer_text), buffer_signs), foll]

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
