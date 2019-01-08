from table_module import TableModule
from module import Module


class ResultModule(Module):
    def __init__(self, lens, freqs, file_path):
        super(Module).__init__()
        self._lens = lens
        self._freqs = freqs
        self._file_path = file_path

    def run(self):
        print('Result Module: Got length and frequency maps, handling')

        # handling lengths and freqs ...
        # ... got this gummy dict:
        result = {'a': 1, 'b': 2, 'c': 3}, {'x': 111, 'y': 222, 'z': 333}

        print('Result Module: Handled, calling Excel Module')
        TableModule(self._lens, self._freqs, result[0], result[1], self._file_path).run()
