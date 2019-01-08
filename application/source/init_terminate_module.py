import queue
import threading

from count_module import CountModule
from phonotype_module import PhonotypeModule
from read_module import ReadModule
from write_module import WriteModule
from module import Module
from pipe import Pipe
from syllabify_module import SyllabifyModule
from clean_module import CleanModule


class InitTerminateModule(Module):

    def __init__(self, file_name, file_path, encoding, language):
        super().__init__()
        self._file_name = file_name
        self._file_path = file_path
        self._encoding = encoding
        self._language = language

    def run(self):
        data = 'conf/conf_uk_cyr'

        read_clean_pipe = Pipe(queue.Queue(), threading.Condition())
        clean_phono_pipe = Pipe(queue.Queue(), threading.Condition())
        phono_syll_pipe = Pipe(queue.Queue(), threading.Condition())
        syll_count_pipe = Pipe(queue.Queue(), threading.Condition())
        count_write_pipe = Pipe(queue.Queue(), threading.Condition())

        read_module = ReadModule([read_clean_pipe], self._file_path, self._encoding, data)
        clean_module = CleanModule([read_clean_pipe, clean_phono_pipe], data)
        phono_module = PhonotypeModule([clean_phono_pipe, phono_syll_pipe], data)
        syll_module = SyllabifyModule([phono_syll_pipe, syll_count_pipe])
        count_module = CountModule([syll_count_pipe, count_write_pipe], data, self._file_path)
        write_module = WriteModule([count_write_pipe], self._file_path)

        print("Process started")

        read_module.run()
        clean_module.start()
        phono_module.start()
        syll_module.start()
        count_module.start()
        write_module.start()

        clean_module.join()
        phono_module.join()
        syll_module.join()
        count_module.join()
        write_module.join()

        print("Process terminated")


if __name__ == '__main__':
    file_path1 = 'inputs/input_uk_cyr.txt'
    file_name1 = 'input_uk_cyr.txt'
    language1 = 'ukrainian'

    encoding1 = "utf-8"
    main = InitTerminateModule(file_name1, file_path1, encoding1, language1)
    main.run()
