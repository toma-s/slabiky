from module import Module
from table_module import TableModule


class ResultModule(Module):
    def __init__(self, lens, freqs, file_path):
        super(Module).__init__()
        self._lens = lens
        self._freqs = freqs
        self._file_path = file_path
        self.map_with_rep = {}
        self.map_wout_rep = {}

    def run(self):
        for it in self._lens:
            if self._lens[it] in self.map_with_rep.keys():
                self.map_with_rep[self._lens[it]] += self._freqs[it]
            else:
                self.map_with_rep[self._lens[it]] = self._freqs[it]
            
        for it in self._lens.values():
            if it in self.map_wout_rep.keys():
                self.map_wout_rep[it] += 1
            else:
                self.map_wout_rep[it] = 1
        TableModule(self._lens, self._freqs, self.map_with_rep, self.map_wout_rep, self._file_path).run()
