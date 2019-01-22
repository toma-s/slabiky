import queue
import threading
import unittest

from application.source import constants
from application.source.clean_module import CleanModule
from application.source.config_data import ConfigData
from application.source.end import End
from application.source.pipe import *
from application.source.word import Text, TextPunctuation


data = ConfigData('../../../config/conf_uk_cyr.json')
pipe_in = Pipe(queue.Queue(), threading.Condition())
pipe_out = Pipe(queue.Queue(), threading.Condition())
module = CleanModule([pipe_in, pipe_out], data)


def run_through_module(words):

    result = []

    for word in words:
        pipe_in.acquire()
        pipe_in.put(word)
        pipe_in.notify()
        pipe_in.release()

    while True:
        pipe_out.acquire()
        if pipe_out.empty():
            pipe_out.wait()
        cleaned_word = pipe_out.get()
        result.append(cleaned_word)
        pipe_out.release()

        if isinstance(cleaned_word, End):
            break

    return result


class TestClean(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        module.start()

    def test_end(self):
        words = [End()]

        result = run_through_module(words)

        self.assertEqual(result, [End()])

    def test_capital(self):
        words = [TextPunctuation('до', [None, None]),
                 TextPunctuation('Києва', [None, None, None, None, None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('до'), Text('києва'), End()])

    def test_non_alphabet(self):
        words = [TextPunctuation('а', [None]),
                 TextPunctuation('foreign', [None, None, None, None, None, None, None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('а'), End()])

    def test_punctuation_only(self):
        words = [TextPunctuation('а', [None]),
                 TextPunctuation('—', [constants.PUNCT]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('а'), End()])

    def test_punctuation_within(self):
        words = [TextPunctuation('а', [None]),
                 TextPunctuation('сло!во', [None, None, None, constants.PUNCT, None, None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('а'), End()])

    def test_quotation(self):
        words = [TextPunctuation('а', [None]),
                 TextPunctuation('«слово»', [constants.PUNCT, None, None, None, None, None, constants.PUNCT]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('а'), Text('слово'), End()])

    def test_hyphen(self):
        words = [TextPunctuation('а', [None]),
                 TextPunctuation('сло-во', [None, None, None, constants.HYPHEN, None, None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('а'), Text('слово'), End()])

    def test_hypnen_at_the_end(self):
        words = [TextPunctuation('а', [None]),
                 TextPunctuation('сло-', [None, None, None, constants.HYPHEN]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('а'), End()])

    def test_hyphen_punctuation(self):
        words = [TextPunctuation('а', [None]),
                 TextPunctuation('сло-во!', [None, None, None, constants.HYPHEN, None, None, constants.PUNCT]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('а'), Text('слово'), End()])

    def test_union_with_prec(self):
        words = [TextPunctuation('українського', [None, None, None, None, None, None,
                                                  None, None, None, None, None, None]),
                 TextPunctuation('ж', [None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('українськогож'), End()])

    def test_union_with_prec_upper(self):
        words = [TextPunctuation('українського', [None, None, None, None, None, None,
                                                  None, None, None, None, None, None]),
                 TextPunctuation('Ж', [None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('українськогож'), End()])

    def test_union_with_foll(self):
        words = [TextPunctuation('з', [None]),
                 TextPunctuation('собою', [None, None, None, None, None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('зсобою'), End()])

    def test_union_with_foll_upper(self):
        words = [TextPunctuation('З', [None]),
                 TextPunctuation('собою', [None, None, None, None, None]),
                 TextPunctuation('слово', [None, None, None, None, None]),
                 TextPunctuation('слово', [None, None, None, None, None]),
                 TextPunctuation('слово', [None, None, None, None, None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('зсобою'), Text('слово'), Text('слово'), Text('слово'), End()])


if __name__ == '__main__':
    unittest.main()
