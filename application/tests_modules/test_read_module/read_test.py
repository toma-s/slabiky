import queue
import threading
import unittest

from application.source.clean_module import CleanModule
from application.source.pipe import *
from application.source.read_module import ReadModule
from application.tests_modules.test_clean_module.test_module import TestModule
from application.tests_modules.test_read_module import expected_outputs


class TestRead(unittest.TestCase):

    def test_read_text(self):
        result = get_items_from_read_module()

        self.assertCountEqual(result, expected_outputs.expected_out_be)
        self.assertListEqual(result, expected_outputs.expected_out_be)

    def test_read_threads(self):
        result = get_items_from_read_module_threads()

        self.assertCountEqual(result, expected_outputs.expected_out_be)
        self.assertListEqual(result, expected_outputs.expected_out_be)


def get_items_from_read_module():
    read_clean_pipe = Pipe(queue.Queue(), threading.Condition())
    file_path = '../../tests/short_texts/belarussian_short_text.txt'
    encoding = 'utf-8'
    data = '../../../config/conf_be_cyr.json'

    read_module = ReadModule([read_clean_pipe], file_path, encoding, data)
    return read_module.read()


def get_items_from_read_module_threads():
    read_test_pipe = Pipe(queue.Queue(), threading.Condition())
    file_path = '../../tests/short_texts/belarussian_short_text.txt'
    encoding = 'utf-8'
    data = '../../../config/conf_be_cyr.json'

    read_module = ReadModule([read_test_pipe], file_path, encoding, data)
    test_module = TestModule([read_test_pipe])

    read_module.run()
    test_module.start()

    test_module.join()

    return test_module.received


if __name__ == '__main__':
    unittest.main()
