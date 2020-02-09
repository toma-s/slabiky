import queue
import threading
import unittest

import constants
from clean_module import CleanModule
from config_data import ConfigData
from end import End
from pipe import *
from word import Text, TextPunctuation

data = ConfigData('../../configs/conf_uk_cyr.json')
pipe_in = Pipe(queue.Queue(), threading.Condition())
pipe_out = Pipe(queue.Queue(), threading.Condition())


def run_through_module(words):
    module = CleanModule([pipe_in, pipe_out], data)
    module.start()
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

    module.join()
    return result


class TestClean(unittest.TestCase):

    def test_end(self):
        words = [End()]

        result = run_through_module(words)

        self.assertEqual(result, [End()])

    def test_capital(self):
        words = [TextPunctuation('Київ', [None, None, None, None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('київ'), End()])

    def test_non_alphabet(self):
        words = [TextPunctuation('foreign', [None, None, None, None, None, None, None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [End()])

    def test_punctuation_only(self):
        words = [TextPunctuation('—', [constants.PUNCT]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [End()])

    def test_punctuation_ending(self):
        words = [TextPunctuation('слово!', [None, None, None, constants.PUNCT, None, None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [End()])

    def test_punctuation_within(self):
        words = [TextPunctuation('сло!во', [None, None, None, constants.PUNCT, None, None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [End()])

    def test_quotation(self):
        words = [TextPunctuation('«слово»', [constants.PUNCT, None, None, None, None, None, constants.PUNCT]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('слово'), End()])

    def test_hyphen(self):
        words = [TextPunctuation('сло-во', [None, None, None, constants.HYPHEN, None, None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('слово'), End()])

    def test_hypnen_at_the_end(self):
        words = [TextPunctuation('сло-', [None, None, None, constants.HYPHEN]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [End()])

    def test_hyphen_punctuation(self):
        words = [TextPunctuation('сло-во!', [None, None, None, constants.HYPHEN, None, None, constants.PUNCT]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('слово'), End()])

    def test_union_with_prec(self):
        words = [TextPunctuation('українського', [None, None, None, None, None, None,
                                                  None, None, None, None, None, None]),
                 TextPunctuation('ж', [None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('українськогож'), End()])

    def test_union_with_prec_first(self):
        words = [TextPunctuation('ж', [None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('ж'), End()])

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

    def test_union_with_foll_last(self):
        words = [TextPunctuation('з', [None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('з'), End()])

    def test_union_with_foll_upper(self):
        words = [TextPunctuation('З', [None]),
                 TextPunctuation('собою', [None, None, None, None, None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('зсобою'), End()])

    def test_apostrophe_U0027(self):
        words = [TextPunctuation('в\'ю', [None, None, None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('в\'ю'), End()])

    def test_apostrophe_U2019(self):
        words = [TextPunctuation('в’ю', [None, None, None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('в’ю'), End()])

    def test_apostrophe_U02BC(self):
        words = [TextPunctuation('вʼю', [None, None, None]),
                 End()]
        result = run_through_module(words)

        self.assertEqual(result, [Text('вʼю'), End()])


if __name__ == '__main__':
    unittest.main()