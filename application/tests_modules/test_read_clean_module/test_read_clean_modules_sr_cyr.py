import queue
import threading
import unittest

from application.source.clean_module import CleanModule
from application.source.config_data import ConfigData
from application.source.end import End
from application.source.pipe import Pipe
from application.source.read_module import ReadModule
from application.source.word import Text

file_path = '../tests/short_texts/serbian_short_text.txt'
encoding = 'utf-8'
data = ConfigData('../../config/conf_sr_cyr.json')

read_clean_pipe = Pipe(queue.Queue(), threading.Condition())
clean_out_pipe = Pipe(queue.Queue(), threading.Condition())


expected_result = [Text('просторе'), Text('данашњег'), Text('панонског'), Text('басена'), Text('некада'), Text('је'), Text('прекривао'), Text('праокеан'), Text('тетис'), Text('чијим'), Text('повлачењем'), Text('је'), Text('и'), Text('настао'), Text('панонски'), Text('басен'), Text('повлачењем'), Text('тетис'), Text('је'), Text('иза'), Text('себе'), Text('оставио'), Text('веома'), Text('плодно'), Text('тло'), Text('па'), Text('се'), Text('због'), Text('тога'), Text('панонски'), Text('басен'), Text('назива'), Text('још'), Text('и'), Text('житницом'), Text('србије'), Text('за'), Text('просторе'), Text('ове'), Text('регије'), Text('особена'), Text('је'), Text('црница'), Text('или'), Text('чернозем'), Text('као'), Text('врста'), Text('земљишта'), Text('међутим'), Text('јавља'), Text('се'), Text('и'), Text('деградирани'), Text('чернозем'), Text('као'), Text('и'), Text('плодно'), Text('алувијално'), Text('тло'), Text('и'), Text('гајњаче'), End()]


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
        print('expected length:', len(expected_result))
        print('actual length:', len(result))

        self.assertCountEqual(result, expected_result)
        self.assertListEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
