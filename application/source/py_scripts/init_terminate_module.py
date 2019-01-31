import queue
import threading

from application.source.count_module import CountModule
from application.source.phonotype_module import PhonotypeModule
from application.source.read_module import ReadModule
from application.source.write_module import WriteModule
from application.source.module import Module
from application.source.pipe import Pipe
from application.source.syllabify_module import SyllabifyModule
from application.source.clean_module import CleanModule


class InitTerminateModule(Module):

    def __init__(self, file_name, file_path, encoding, language):
        super().__init__()
        self._file_name = file_name
        self._file_path = file_path
        self._encoding = encoding
        self._language = language

    def run(self):
        dummy_data = 'conf/conf_uk_cyr'

        read_clean_pipe = Pipe(queue.Queue(), threading.Condition())
        clean_phono_pipe = Pipe(queue.Queue(), threading.Condition())
        phono_syll_pipe = Pipe(queue.Queue(), threading.Condition())
        syll_count_pipe = Pipe(queue.Queue(), threading.Condition())
        count_write_pipe = Pipe(queue.Queue(), threading.Condition())

        read_module = ReadModule([read_clean_pipe], self._file_path, self._encoding, dummy_data)
        clean_module = CleanModule([read_clean_pipe, clean_phono_pipe], dummy_data)
        phono_module = PhonotypeModule([clean_phono_pipe, phono_syll_pipe], dummy_data)
        syll_module = SyllabifyModule([phono_syll_pipe, syll_count_pipe])
        count_module = CountModule([syll_count_pipe, count_write_pipe], dummy_data, self._file_path)
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
