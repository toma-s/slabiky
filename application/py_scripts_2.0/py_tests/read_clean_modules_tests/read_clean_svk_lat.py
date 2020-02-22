import queue
import threading
import unittest

from clean_module import CleanModule
from config_data import ConfigData
from end import End
from pipe import Pipe
from read_module import ReadModule
from word import Text

file_path = '../test_files/slovak/test_slovak.txt'
encoding = 'utf-8-sig'
data = ConfigData('../../configs/conf_svk_lat.json')

read_clean_pipe = Pipe(queue.Queue(), threading.Condition())
clean_out_pipe = Pipe(queue.Queue(), threading.Condition())

expected_result = [Text('toto'), Text('je'), Text('prvá'), Text('veta'), Text('#tomobil'), Text('ide'), Text('posledné'), Text('slovo'), Text('má'), Text('byť'), Text('vyhodené'), Text('slovo'), End()]


def get_from_module(pipe_out):
    read_module = ReadModule([read_clean_pipe], file_path, encoding, data)
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
    clean_module = CleanModule([read_clean_pipe, clean_out_pipe], data)
    clean_module.start()
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

    clean_module.join()
    return result


class TestReadCleanModules(unittest.TestCase):

    def test_text(self):
        words = get_from_module(read_clean_pipe)
        result = run_through_module(words)
        print(result)

        self.assertCountEqual(result, expected_result)
        self.assertListEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
