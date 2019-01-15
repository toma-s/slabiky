import queue
import threading
import unittest

from application.source.pipe import *
from application.source.read_module import ReadModule
from application.tests_modules.test_read_module import expected_outputs


class TestReadBelarussian(unittest.TestCase):

    def test_read_text_be(self):
        read_clean_pipe = Pipe(queue.Queue(), threading.Condition())
        file_path = '../../tests/short_texts/belarussian_short_text.txt'
        encoding = 'utf-8'
        data = '../../../config/conf_be_cyr.json'

        read_module = ReadModule([read_clean_pipe], file_path, encoding, data)
        result = read_module.read()

        self.assertCountEqual(result, expected_outputs.expected_out_be)
        self.assertListEqual(result, expected_outputs.expected_out_be)


if __name__ == '__main__':
    unittest.main()
