import queue
import threading
import unittest

from application.source.config_data import ConfigData
from application.source.pipe import *
from application.source.read_module import ReadModule
from application.tests_modules.test_clean_module.test_module import TestModule
from application.tests_modules.test_read_module import expected_outputs


class TestRead(unittest.TestCase):
    file_path = '../../tests/short_texts/belarussian_short_text.txt'
    encoding = 'utf-8'
    data = ConfigData('../../../config/conf_be_cyr.json')

    def test_read_text(self):
        result = self.get_items_from_read_module()

        self.assertCountEqual(result, expected_outputs.expected_out_be)
        self.assertListEqual(result, expected_outputs.expected_out_be)

    def test_read_threads(self):
        result = self.get_items_from_read_module_threads()

        self.assertCountEqual(result, expected_outputs.expected_out_be)
        self.assertListEqual(result, expected_outputs.expected_out_be)

    # Utility functions

    def get_items_from_read_module(self):
        read_clean_pipe = Pipe(queue.Queue(), threading.Condition())

        read_module = ReadModule([read_clean_pipe], self.file_path, self.encoding, self.data)
        return read_module.read()

    def get_items_from_read_module_threads(self):
        read_test_pipe = Pipe(queue.Queue(), threading.Condition())

        read_module = ReadModule([read_test_pipe], self.file_path, self.encoding, self.data)
        test_module = TestModule([read_test_pipe])

        read_module.run()
        test_module.start()

        test_module.join()

        return test_module.received


if __name__ == '__main__':
    unittest.main()
