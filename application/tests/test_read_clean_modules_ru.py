import queue
import threading
import unittest

from application.source.clean_module import CleanModule
from application.source.config_data import ConfigData
from application.source.end import End
from application.source.pipe import Pipe
from application.source.read_module import ReadModule
from application.source.word import Text

# file_path = '../tests/short_texts/custom_text.txt'
file_path = '../tests/short_texts/russian_short_text.txt'
encoding = 'utf-8'
data = ConfigData('../../config/conf_ru_cyr.json')

read_clean_pipe = Pipe(queue.Queue(), threading.Condition())
clean_out_pipe = Pipe(queue.Queue(), threading.Condition())

# Россия, официально также Российская Федерация — государство в Восточной Европе, Центральной и Северной Азии. Территория России в рамках её конституционного устройства составляет 17 125 191 км²; население страны (в пределах её заявленной территории) составляет 146 880 432 чел. (2018). Занимает первое место в мире по территории, шестое — по объёму ВВП по ППС и девятое — по численности населения. Столица — Москва. Государственный язык — русский.

expected_result = [Text('россия'), Text('официально'), Text('также'), Text('российская'), Text('федерация'), Text('государство'), Text('ввосточной'), Text('европе'), Text('центральной'), Text('и'), Text('северной'), Text('азии'), Text('территория'), Text('россии'), Text('врамках'), Text('её'), Text('конституционного'), Text('устройства'), Text('составляет'), Text('население'), Text('страны'), Text('впределах'), Text('её'), Text('заявленной'), Text('территории'), Text('составляет'), Text('занимает'), Text('первое'), Text('место'), Text('вмире'), Text('по'), Text('территории'), Text('шестое'), Text('по'), Text('объёму'), Text('по'), Text('и'), Text('девятое'), Text('по'), Text('численности'), Text('населения'), Text('столица'), Text('москва'), Text('государственный'), Text('язык'), Text('русский'), End()]


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
