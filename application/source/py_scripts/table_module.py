from application.source.module import Module


class TableModule(Module):
    def __init__(self, map_len, map_freq, map_with_rep, map_wout_rep, file_path):
        super(Module).__init__()
        self._map_len = map_len
        self._map_freq = map_freq
        self._map_with_rep = map_with_rep
        self._map_wout_rep = map_wout_rep
        self._file_path = file_path

    def run(self):
        print('Module Result: Got length and frequency maps, handling')
        self.write_to_excel()
        print('Module Result: Written to Excel, finished')

    def write_to_excel(self):
        pass

