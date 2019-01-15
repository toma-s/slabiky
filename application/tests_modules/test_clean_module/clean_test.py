import queue
import threading
import unittest

from application.source.end import End
from application.source.pipe import *
from application.source.read_module import ReadModule
from application.source.clean_module import CleanModule
from application.source.word import Text, TextPunctuation
from application.tests_modules.test_clean_module import expected_outputs
from application.tests_modules.test_clean_module.test_module import TestModule


class TestCleanBelarussian(unittest.TestCase):

    def test_clean_words_be(self):
        words = get_items_from_read_module()

        read_clean_pipe = Pipe(queue.Queue(), threading.Condition())
        clean_phono_pipe = Pipe(queue.Queue(), threading.Condition())
        data = '../../../config/conf_be_cyr.json'

        clean_module = CleanModule([read_clean_pipe, clean_phono_pipe], data)
        result = []
        prec, curr, foll = None, None, None
        for word in words:
            if word is None:
                continue
            prec = curr
            curr = foll
            foll = word
            if isinstance(curr, TextPunctuation):
                cleaned = clean_module.clean([prec, curr, foll])
                prec = cleaned[0]
                curr = cleaned[1]
                foll = cleaned[2]
                if curr:
                    result.append(Text(curr.get_text()))
            if isinstance(word, End):
                result.append(word)

        self.assertCountEqual(result, expected_outputs.expected_out_be)
        self.assertListEqual(result, expected_outputs.expected_out_be)

    def test_clean_threading_be(self):
        result = get_items_from_read_clean_modules()

        self.assertCountEqual(result, expected_outputs.expected_out_be)
        self.assertEqual(result, expected_outputs.expected_out_be)


def get_items_from_read_module():
    read_clean_pipe = Pipe(queue.Queue(), threading.Condition())
    file_path = '../../tests/short_texts/belarussian_short_text.txt'
    encoding = 'utf-8'
    data = '../../../config/conf_be_cyr.json'

    read_module = ReadModule([read_clean_pipe], file_path, encoding, data)
    return read_module.read()


def get_items_from_read_clean_modules():
    read_clean_pipe = Pipe(queue.Queue(), threading.Condition())
    clean_test_pipe = Pipe(queue.Queue(), threading.Condition())
    file_path = '../../tests/short_texts/belarussian_short_text.txt'
    encoding = 'utf-8'
    data = '../../../config/conf_be_cyr.json'

    read_module = ReadModule([read_clean_pipe], file_path, encoding, data)
    clean_module = CleanModule([read_clean_pipe, clean_test_pipe], data)
    test_module = TestModule([clean_test_pipe])

    read_module.run()
    clean_module.start()
    test_module.start()

    clean_module.join()
    test_module.join()

    return test_module.received


if __name__ == '__main__':
    unittest.main()
