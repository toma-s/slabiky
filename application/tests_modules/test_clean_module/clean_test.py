import queue
import threading
import unittest

from application.source import constants
from application.source.config_data import ConfigData
from application.source.end import End
from application.source.pipe import *
from application.source.clean_module import CleanModule
from application.source.word import Text, TextPunctuation


data = ConfigData('../../../config/conf_uk_cyr.json')
pipe_in = Pipe(queue.Queue(), threading.Condition())
pipe_out = Pipe(queue.Queue(), threading.Condition())
module = CleanModule([pipe_in, pipe_out], data)


def run_through_module(words):

    result = []

    for word in words:
        print('word:', word)
        pipe_in.acquire()
        pipe_in.put(word)
        pipe_in.notify()
        pipe_in.release()

    while True:
        pipe_out.acquire()
        if pipe_out.empty():
            pipe_out.wait()
        cleaned_word = pipe_out.get()
        print('cleaned_word:', cleaned_word)
        result.append(cleaned_word)
        pipe_out.release()

        if isinstance(cleaned_word, End):
            break

    return result


class TestClean(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        module.start()

    @classmethod
    def tearDownClass(cls):
        module.join()

    def test_clean_end(self):
        words = [End()]

        result = run_through_module(words)
        print(result)

        self.assertEqual(result, [End()])

    def test_clean_capital(self):
        words = [TextPunctuation('а', [None]),
                 TextPunctuation('зПольским', [None, None, None, None, None, None, None, None, None]),
                 End()]

        result = run_through_module(words)
        print(result)

        self.assertEqual(result, [Text('а'), Text('зпольским'), End()])

    def test_clean_non_alphabet(self):
        words = [TextPunctuation('а', [None]),
                 TextPunctuation('dummy', [None, None, None, None, None]),
                 End()]

        result = run_through_module(words)
        print(result)

        self.assertEqual(result, [Text('а'), End()])

    def test_clean_punctuation_only(self):
        words = [TextPunctuation('а', [None]),
                 TextPunctuation('—', [constants.PUNCT]),
                 End()]

        result = run_through_module(words)
        print(result)

        self.assertEqual(result, [Text('а'), End()])

    def test_clean_punctuation_within(self):
        words = [TextPunctuation('а', [None]),
                 TextPunctuation('сло!во', [None, None, None, constants.PUNCT, None, None]),
                 End()]

        result = run_through_module(words)
        print(result)

        self.assertEqual(result, [Text('а'), End()])

    def test_clean_quotation(self):
        words = [TextPunctuation('а', [None]),
                 TextPunctuation('«слово»', [constants.PUNCT, None, None, None, None, None, constants.PUNCT]),
                 End()]

        result = run_through_module(words)
        print(result)

        self.assertEqual(result, [Text('а'), Text('слово'), End()])

    def test_clean_hyphen(self):
        words = [TextPunctuation('а', [None]),
                 TextPunctuation('сло-во', [None, None, None, constants.HYPHEN, None, None]),
                 End()]

        result = run_through_module(words)
        print(result)

        self.assertEqual(result, [Text('а'), Text('слово'), End()])

    def test_clean_hyphen_punctuation(self):
        words = [TextPunctuation('а', [None]),
                 TextPunctuation('сло-во!', [None, None, None, constants.HYPHEN, None, None, constants.PUNCT]),
                 End()]

        result = run_through_module(words)
        print(result)

        self.assertEqual(result, [Text('а'), Text('слово'), End()])


if __name__ == '__main__':
    unittest.main()
