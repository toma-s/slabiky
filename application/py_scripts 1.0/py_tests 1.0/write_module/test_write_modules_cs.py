from pipe import Pipe
from queue import Queue
from threading import Condition
from write_module import WriteModule
from word import SyllablesLengths
from end import End
import unittest
import time
import os.path

words_to_do = [[End()],
               
               [SyllablesLengths(["pou", "ze"], [2, 2]),
               SyllablesLengths(["fa", "rma", "ceu", "ti", "cký"], [2, 3, 2, 2, 3]),
               End()],
               
               [SyllablesLengths(["sněh"], [3])] * 1000]

syllables = ["pou-ze fa-rma-ceu-ti-cký",
             "sněh " * 999 + "sněh"]

lengths = ["2-2 2-3-2-2-3",
           "3 " * 999 + "3"]

file_path = "blabla/"

file_syllables = file_path + "syllable_text.txt"

file_lengths = file_path + "syllable_lengths_text.txt"


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reset()
        module.start()
        print("reset")
            
##    def test1(self):
##        for word in words_to_do[0]:
##            run_through_module(word, module)
##        time.sleep(1)
##        self.assertEqual(os.path.exists(file_lengths), False)
##        self.assertEqual(os.path.exists(file_syllables), False)
##        reset()
##        module.reset()

    def test2(self):
        pin = Pipe(Queue(), Condition())
        pipe_syllabify_count = Pipe(Queue(), Condition())
        pout = Pipe(Queue(), Condition())
        module = WriteModule([pipe_syllabify_count, pout], file_path)
        module.start()
        for word in words_to_do[0]:
            run_through_module(word, module)
        time.sleep(1)
        self.assertEqual(os.path.exists(file_lengths), True)
        self.assertEqual(os.path.exists(file_syllables), True)
        self.assertEqual(text_of_file(file_syllables), syllables[1])
        self.assertEqual(text_of_file(file_lengths), lengths[1])
##        for word in words_to_do[1]:
##            run_through_module(word, module)
##        time.sleep(1)
##        self.assertEqual(os.path.exists(file_lengths), True)
##        self.assertEqual(os.path.exists(file_syllables), True)
##        self.assertEqual(text_of_file(file_syllables), syllables[0])
##        self.assertEqual(text_of_file(file_lengths), lengths[0])
##        module.reset()

##    def test3(self):
        
##        reset()
##        module.reset()

    
        
def reset():
    if os.path.isfile(file_syllables):
        os.remove(file_syllables)
    if os.path.isfile(file_lengths):
        os.remove(file_lengths)

def text_of_file(file):
    with open(file, "r", encoding="utf-8") as f:
        text = ""
        for line in f:
            text += line
    f.close()
    return text
            

def run_through_module(word, mod):
    pin = mod.get_pipes()[0]
    pin.acquire()
    pin.put(word)
    pin.notify()
    pin.release()


pin = Pipe(Queue(), Condition())
pipe_syllabify_count = Pipe(Queue(), Condition())
pout = Pipe(Queue(), Condition())
module = WriteModule([pipe_syllabify_count, pout], file_path)

if __name__ == "__main__":
    unittest.main()




