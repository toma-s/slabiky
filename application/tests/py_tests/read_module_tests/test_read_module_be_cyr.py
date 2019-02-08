import queue
import threading
import unittest

from application.py_scripts import constants
from application.py_scripts.config_data import ConfigData
from application.py_scripts.end import End
from application.py_scripts.pipe import *
from application.py_scripts.read_module import ReadModule
from application.py_scripts.word import TextPunctuation


file_path = '../test_files/belarusian/test_belarusian.txt'
# file_path = '../test_files/belarusian/temp.txt'
encoding = 'utf-8'
data = ConfigData('../../../py_scripts/configs/conf_be_cyr.json')

pipe_out = Pipe(queue.Queue(), threading.Condition())
module = ReadModule([pipe_out], file_path, encoding, data)

# expected_result = [TextPunctuation('стык', [None, None, None, None]), TextPunctuation('марфем...', [None, None, None, None, None, None, constants.PUNCT, constants.PUNCT, constants.PUNCT]), End()]

expected_result = [TextPunctuation('У', [None]), TextPunctuation('беларускай', [None, None, None, None, None, None, None, None, None, None]), TextPunctuation('мове', [None, None, None, None]), TextPunctuation('зычныя', [None, None, None, None, None, None]), TextPunctuation('могуць', [None, None, None, None, None, None]), TextPunctuation('адрознівацца', [None, None, None, None, None, None, None, None, None, None, None, None]), TextPunctuation('даўжынёй', [None, None, None, None, None, None, None, None]), TextPunctuation('гучання,', [None, None, None, None, None, None, None, constants.PUNCT]), TextPunctuation('якая', [None, None, None, None]), TextPunctuation('пака-звае', [None, None, None, None, constants.HYPHEN, None, None, None, None]), TextPunctuation('на', [None, None]), TextPunctuation('стык', [None, None, None, None]), TextPunctuation('марфем...', [None, None, None, None, None, None, constants.PUNCT, constants.PUNCT, constants.PUNCT]), TextPunctuation('Пераважная', [None, None, None, None, None, None, None, None, None, None]), TextPunctuation('‚колькасць‘', [constants.PUNCT, None, None, None, None, None, None, None, None, None, constants.PUNCT]), TextPunctuation('гукаў', [None, None, None, None, None]), TextPunctuation('утвараюцца', [None, None, None, None, None, None, None, None, None, None]), TextPunctuation('ў', [None]), TextPunctuation('цэнтры', [None, None, None, None, None, None]), TextPunctuation('ротавай', [None, None, None, None, None, None, None]), TextPunctuation('поласці', [None, None, None, None, None, None, None]), TextPunctuation('пры', [None, None, None]), TextPunctuation('высокім', [None, None, None, None, None, None, None]), TextPunctuation('агульным', [None, None, None, None, None, None, None, None]), TextPunctuation('пад’ёме', [None, None, None, None, None, None, None]), TextPunctuation('языка.', [None, None, None, None, None, constants.PUNCT]), TextPunctuation('Вялікае', [None, None, None, None, None, None, None]), TextPunctuation('Ducatus', [None, None, None, None, None, None, None]), TextPunctuation('Lithuaniae', [None, None, None, None, None, None, None, None, None, None]), TextPunctuation('знаходзілася', [None, None, None, None, None, None, None, None, None, None, None, None]), TextPunctuation('ў', [None]), TextPunctuation('дынастычнай', [None, None, None, None, None, None, None, None, None, None, None]), TextPunctuation('уніі', [None, None, None, None]), TextPunctuation('—', [constants.PUNCT]), TextPunctuation('з', [None]), TextPunctuation('Польскім', [None, None, None, None, None, None, None, None]), TextPunctuation('кара-леўствам!', [None, None, None, None, constants.HYPHEN, None, None, None, None, None, None, None, None, constants.PUNCT]), End()]


def get_from_module():

    module.run()
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


class TestRead(unittest.TestCase):

    def test_text(self):
        result = get_from_module()
        print(result)

        self.assertCountEqual(result, expected_result)
        self.assertListEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()