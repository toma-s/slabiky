import queue
import threading
import unittest

from application.source.clean_module import CleanModule
from application.source.config_data import ConfigData
from application.source.end import End
from application.source.pipe import Pipe
from application.source.read_module import ReadModule
from application.source.word import Text

file_path = '../tests/short_texts/belarussian_short_text.txt'
encoding = 'utf-8'
data = ConfigData('../../config/conf_be_cyr.json')

read_clean_pipe = Pipe(queue.Queue(), threading.Condition())
clean_out_pipe = Pipe(queue.Queue(), threading.Condition())

read_module = ReadModule([read_clean_pipe], file_path, encoding, data)
clean_module = CleanModule([read_clean_pipe, clean_out_pipe], data)

expected_result = [Text('у'), Text('беларускай'), Text('мове'), Text('зычныя'), Text('могуць'), Text('адрознівацца'), Text('даўжынёй'), Text('гучання'), Text('якая'), Text('паказвае'), Text('на'), Text('стык'), Text('марфем'), Text('пераважная'), Text('колькасць'), Text('гукаў'), Text('утвараюццаў'), Text('цэнтры'), Text('ротавай'), Text('поласці'), Text('пры'), Text('высокім'), Text('агульным'), Text('пад’ёме'), Text('языка'), Text('вялікае'), Text('знаходзіласяў'), Text('дынастычнай'), Text('уніі'), Text('зпольскім'), Text('каралеўствам'), End()]


def get_from_module(pipe_out):

    read_module.run()
    result = []

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


def run_through_module(words):

    result = []

    for word in words:
        read_clean_pipe.acquire()
        read_clean_pipe.put(word)
        read_clean_pipe.notify()
        read_clean_pipe.release()

    while True:
        clean_out_pipe.acquire()
        if clean_out_pipe.empty():
            clean_out_pipe.wait()
        cleaned_word = clean_out_pipe.get()
        result.append(cleaned_word)
        clean_out_pipe.release()

        if isinstance(cleaned_word, End):
            break

    return result


class TestReadCleanModules(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        read_module.run()
        clean_module.start()

    @classmethod
    def tearDownClass(cls):
        clean_module.join()

    def test_text(self):
        words = get_from_module(read_clean_pipe)
        result = run_through_module(words)

        self.assertCountEqual(result, expected_result)
        self.assertListEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
