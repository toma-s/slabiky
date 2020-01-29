from end import End
from thread_module import ThreadModule


class WriteModule(ThreadModule):
    def __init__(self, pipes, file_path):
        super().__init__(pipes)
        self._file_path = file_path
        self._syllables = ""
        self._lenghts = ""
        self._count = 0
        self._spacer = ""

    def run(self):
        pipe_in = self.get_pipes()[0]
        while True:
            pipe_in.acquire()
            if pipe_in.empty():
                pipe_in.wait()
            word = pipe_in.get()
            pipe_in.release()
            if isinstance(word, End):
                if self._spacer == "" and self._lenghts == "" and self._syllables == "":
                    self._lenghts = "input error"
                    self._syllables = "input error"
                self.write_to_file()
                break
            else:
                self.store(word)

    def store(self, word):
        self.add_spacer()
        for it in word.get_syllables():
            self._syllables += it
            self._syllables += "-"
        for it in word.get_lengths():
            self._lenghts += str(it)
            self._lenghts += "-"
        self.delete_last_char()
        self._count += 1
        if self._count == 1000:
            self.write_to_file()
            self.clear()

    def add_spacer(self):
        self._syllables += self._spacer
        self._lenghts += self._spacer
        self._spacer = " "

    def delete_last_char(self):
        self._syllables = self._syllables[:-1]
        self._lenghts = self._lenghts[:-1]

    def write_to_file(self):
        with open(self._file_path + "syllable_text.txt", "ab") as f:
            u = u"{}".format(self._syllables)
            f.write(u.encode("utf-8"))
        f.close()
        with open(self._file_path + "syllable_lengths_text.txt", "a") as f:
            f.write(self._lenghts)
        f.close()

    def clear(self):
        self._syllables = ""
        self._lenghts = ""
        self._count = 0

    def reset(self):
        self._syllables = ""
        self._lenghts = ""
        self._count = 0
        self._spacer = ""
