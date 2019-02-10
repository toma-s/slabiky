from phonotype_module import PhonotypeModule
from syllabify_module import SyllabifyModule
from clean_module import CleanModule
from count_module import CountModule
from write_module import WriteModule
from read_module import ReadModule
from config_data import ConfigData
from threading import Condition
from module import Module
from queue import Queue
from pipe import Pipe
import sys


class InitTerminateModule(Module):

    def __init__(self, file_name, file_path, encoding, language):
        super().__init__()
        self.data             = ConfigData(language) # TODO
        self.file_name        = file_name
        self.file_path        = file_path
        self.encoding         = encoding

        self.pipe_read_clean  = Pipe(Queue(), Condition())
        self.pipe_clean_sound = Pipe(Queue(), Condition())
        self.pipe_sound_syll  = Pipe(Queue(), Condition())
        self.pipe_syll_count  = Pipe(Queue(), Condition())
        self.pipe_count_txt   = Pipe(Queue(), Condition())

    def run(self):
        data = self.data

        read_module_pipes = [self.pipe_read_clean]
        read_module = ReadModule(read_module_pipes, self.file_path + self.file_name, self.encoding, data)

        clean_module_pipes = [self.pipe_read_clean, self.pipe_clean_sound]
        clean_module = CleanModule(clean_module_pipes, data)

        phonoype_module_pipes = [self.pipe_clean_sound, self.pipe_sound_syll]
        phonotype_module = PhonotypeModule(phonoype_module_pipes, data)

        syllabify_module_pipes = [self.pipe_sound_syll, self.pipe_syll_count]
        syllabify_module = SyllabifyModule(syllabify_module_pipes)

        count_module_pipes = [self.pipe_syll_count, self.pipe_count_txt]
        count_module = CountModule(count_module_pipes, data, self.file_path)

        write_module_pipes = [self.pipe_count_txt]
        write_module = WriteModule(write_module_pipes, self.file_path)

        clean_module.start()
        phonotype_module.start()
        syllabify_module.start()
        count_module.start()
        write_module.start()

        read_module.run()

        phonotype_module.join()
        syllabify_module.join()
        count_module.join()
        write_module.join()


##if __name__ == '__main__':
main = InitTerminateModule(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
#    main = InitTerminateModule('test.txt', 'C:/wamp64/www/tis/temp_files/test/', 'UTF-8-sig', 'C:/wamp64/www/tis/configs/conf_cs_lat.json')

##main = InitTerminateModule('test_czech.txt', 'C:/wamp64/www/tis/temp_files/tmpe45a3818593caddae5e9fc8f5b9311de/', 'UTF-8', 'C:/wamp64/www/tis/configs/conf_cs_lat.json')
       
main.run()

    

