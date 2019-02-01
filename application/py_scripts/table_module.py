from module import Module
import xlwt


class TableModule(Module):
    def __init__(self, map_len, map_freq, map_with_rep, map_wout_rep, file_path):
        super(Module).__init__()
        self._map_len = map_len
        self._map_freq = map_freq
        self._map_with_rep = map_with_rep
        self._map_wout_rep = map_wout_rep
        self._file_path = file_path

    def run(self):
        self.write_to_excel()

    def write_to_excel(self):
        self.write_syllables_multiplicity()
        self.write_number_of_length_of_syllables_with_repetition()
        self.write_number_of_length_of_syllables_without_repetition()        

    def write_syllables_multiplicity(self):
        a = []
        wb = xlwt.Workbook()
        sheet1 = wb.add_sheet("Sheet1")
        self.write_three_names_of_colums(sheet1)
        for it in self._map_freq:
            a.append((it, self._map_freq[it], self._map_len[it]))
        a = sorted(a,key=lambda x:(-x[1], x[0]))
        self.write_row(sheet1, a, 3)
        wb.save(self._file_path + "syllables_multiplicity.xls")

    def write_number_of_length_of_syllables_with_repetition(self):
        a = []
        wb = xlwt.Workbook()
        sheet1 = wb.add_sheet("Sheet1")
        self.write_two_names_of_colums(sheet1)
        for it in self._map_with_rep:
            a.append((it, self._map_with_rep[it]))
        a = sorted(a,key=lambda x:(x[0]))
        self.write_row(sheet1, a, 2)
        wb.save(self._file_path + "number_of_length_of_syllables_with_repetition.xls")

    def write_number_of_length_of_syllables_without_repetition(self):
        a = []
        wb = xlwt.Workbook()
        sheet1 = wb.add_sheet("Sheet1")
        self.write_two_names_of_colums(sheet1)
        for it in self._map_wout_rep:
            a.append((it, self._map_wout_rep[it]))
        a = sorted(a,key=lambda x:(x[0]))
        self.write_row(sheet1, a, 2)
        wb.save(self._file_path + "number_of_length_of_syllables_without_repetition.xls")


    def write_two_names_of_colums(self, sheet1):
        sheet1.write(0, 0, "length of syllable")
        sheet1.write(0, 1, "multiplicity")

    def write_three_names_of_colums(self, sheet1):
        sheet1.write(0, 0, "syllable")
        sheet1.write(0, 1, "multiplicity")
        sheet1.write(0, 2, "length of syllable")

    def write_row(self, sheet1, a, count):
        for i in range(len(a)):
            for j in range(count):
                sheet1.write(i+1, j, a[i][j])
