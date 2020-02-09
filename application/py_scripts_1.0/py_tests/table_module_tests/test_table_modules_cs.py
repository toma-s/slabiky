from table_module import TableModule
import unittest
import time
import xlrd

list_lengths_map = [{'au': 1, 'bi': 2, 'ceu': 2, 'cký': 3, 'dem': 3, 'do': 2, 'fa': 2, 'gi': 2, 'je': 2, 'jo': 2,
               'lo': 2, 'ma': 2, 'mí': 2, 'na': 2, 'ne': 2, 'o': 1, 'po': 2, 'pou': 2, 'rma': 3, 'sex': 4,
               'sm': 2, 'sro': 3, 'ti': 2, 'to': 2, 'tý': 2, 'u': 1, 'ur': 2, 'vl': 2, 'vě': 3, 'ze': 2,
               'či': 2, 'zpa': 3, 'žil': 3},
                    {'wro': 3, 'bl': 2, 'sněh': 3},
                    {'у': 1, 'кра': 3, 'їн': 3, 'сько': 3, 'гож': 3},
                    {'rž': 2},
                    {'ma': 2, 'ria': 3}]

list_frequency_map = [{'au': 1, 'bi': 1, 'ceu': 1, 'cký': 2, 'dem': 1, 'do': 1, 'fa': 1, 'gi': 1, 'je': 1, 'jo': 1,
                 'lo': 1, 'ma': 1, 'mí': 1, 'na': 1, 'ne': 1, 'o': 1, 'po': 1, 'pou': 1, 'rma': 1, 'sex': 1,
                 'sm': 1, 'sro': 1, 'ti': 2, 'to': 1, 'tý': 1, 'u': 1, 'ur': 1, 'vl': 1, 'vě': 1, 'ze': 1,
                 'či': 1, 'zpa': 1, 'žil': 1},
                      {'wro': 1, 'bl': 1, 'sněh': 1},
                      {'у': 1, 'кра': 1, 'їн': 1, 'сько': 1, 'гож': 1},
                      {'rž': 1},
                      {'ma': 1, 'ria': 1}]

list_map_with_rep = [{1: 3, 2: 23, 3: 8, 4: 1},
                     {3: 2, 2: 1},
                     {1: 1, 3: 4},
                     {2: 1},
                     {2: 1, 3: 1}]

list_map_wout_rep = [{1: 3, 2: 22, 3: 7, 4: 1},
                     {3: 2, 2: 1},
                     {1: 1, 3: 4},
                     {2: 1},
                     {2: 1, 3: 1}]

file_path = "blabla/"

syllables_multiplicity = [[['syllable', 'cký', 'ti', 'au', 'bi', 'ceu', 'dem', 'do', 'fa', 'gi', 'je', 'jo', 'lo', 'ma', 'mí', 'na', 'ne', 'o', 'po', 'pou', 'rma', 'sex', 'sm', 'sro', 'to', 'tý', 'u', 'ur', 'vl', 'vě', 'ze', 'zpa', 'či', 'žil'],
                          ['multiplicity', 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                          ['length of syllable', 3.0, 2.0, 1.0, 2.0, 2.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 2.0, 2.0, 3.0, 4.0, 2.0, 3.0, 2.0, 2.0, 1.0, 2.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0]],

                          [['syllable', 'bl', 'sněh', 'wro'],
                           ['multiplicity', 1.0, 1.0, 1.0],
                           ['length of syllable', 2.0, 3.0, 3.0]],

                          [['syllable', 'гож', 'кра', 'сько', 'у', 'їн'],
                           ['multiplicity', 1.0, 1.0, 1.0, 1.0, 1.0],
                           ['length of syllable', 3.0, 3.0, 3.0, 1.0, 3.0]],

                          [['syllable', 'rž'],
                           ['multiplicity', 1.0],
                           ['length of syllable', 2.0]],

                          [['syllable', 'ma', 'ria'],
                           ['multiplicity', 1.0, 1.0],
                           ['length of syllable', 2.0, 3.0]]]

number_of_length_of_syllables_with_repetition = [[['length of syllable', 1.0, 2.0, 3.0, 4.0],
                                                 ['multiplicity', 3.0, 23.0, 8.0, 1.0]],

                                                 [['length of syllable', 2.0, 3.0],
                                                  ['multiplicity', 1.0, 2.0]],

                                                 [['length of syllable', 1.0, 3.0],
                                                  ['multiplicity', 1.0, 4.0]],

                                                 [['length of syllable', 2.0],
                                                  ['multiplicity', 1.0]],
                                                 
                                                 [['length of syllable', 2.0, 3.0],
                                                  ['multiplicity', 1.0, 1.0]]]

number_of_length_of_syllables_without_repetition = [[['length of syllable', 1.0, 2.0, 3.0, 4.0],
                                                     ['multiplicity', 3.0, 22.0, 7.0, 1.0]],

                                                    [['length of syllable', 2.0, 3.0],
                                                     ['multiplicity', 1.0, 2.0]],
                                                    
                                                    [['length of syllable', 1.0, 3.0],
                                                     ['multiplicity', 1.0, 4.0]],

                                                    [['length of syllable', 2.0],
                                                     ['multiplicity', 1.0]],

                                                     [['length of syllable', 2.0, 3.0],
                                                      ['multiplicity', 1.0, 1.0]]]

class TestStringMethods(unittest.TestCase):

    def test_1(self):
        module = TableModule(list_lengths_map[0], list_frequency_map[0], list_map_with_rep[0], list_map_wout_rep[0], file_path)
        module.run()
        time.sleep(1)
        data = xlrd.open_workbook(file_path + 'syllables_multiplicity.xls')
        table = data.sheets()[0]        
        self.assertEqual(table.col_values(0), syllables_multiplicity[0][0])
        self.assertEqual(table.col_values(1), syllables_multiplicity[0][1])
        self.assertEqual(table.col_values(2), syllables_multiplicity[0][2])
        data = xlrd.open_workbook(file_path + 'number_of_length_of_syllables_with_repetition.xls')
        table = data.sheets()[0]
        self.assertEqual(table.col_values(0), number_of_length_of_syllables_with_repetition[0][0])
        self.assertEqual(table.col_values(1), number_of_length_of_syllables_with_repetition[0][1])
        data = xlrd.open_workbook(file_path + 'number_of_length_of_syllables_without_repetition.xls')
        table = data.sheets()[0]
        self.assertEqual(table.col_values(0), number_of_length_of_syllables_without_repetition[0][0])
        self.assertEqual(table.col_values(1), number_of_length_of_syllables_without_repetition[0][1])

    def test_2(self):
        module = TableModule(list_lengths_map[1], list_frequency_map[1], list_map_with_rep[1], list_map_wout_rep[1], file_path)
        module.run()
        time.sleep(1)
        data = xlrd.open_workbook(file_path + 'syllables_multiplicity.xls')
        table = data.sheets()[0] 
        self.assertEqual(table.col_values(0), syllables_multiplicity[1][0])
        self.assertEqual(table.col_values(1), syllables_multiplicity[1][1])
        self.assertEqual(table.col_values(2), syllables_multiplicity[1][2])
        data = xlrd.open_workbook(file_path + 'number_of_length_of_syllables_with_repetition.xls')
        table = data.sheets()[0]
        self.assertEqual(table.col_values(0), number_of_length_of_syllables_with_repetition[1][0])
        self.assertEqual(table.col_values(1), number_of_length_of_syllables_with_repetition[1][1])
        data = xlrd.open_workbook(file_path + 'number_of_length_of_syllables_without_repetition.xls')
        table = data.sheets()[0]
        self.assertEqual(table.col_values(0), number_of_length_of_syllables_without_repetition[1][0])
        self.assertEqual(table.col_values(1), number_of_length_of_syllables_without_repetition[1][1])

    def test_3(self):
        module = TableModule(list_lengths_map[2], list_frequency_map[2], list_map_with_rep[2], list_map_wout_rep[2], file_path)
        module.run()
        time.sleep(1)
        data = xlrd.open_workbook(file_path + 'syllables_multiplicity.xls')
        table = data.sheets()[0]
        self.assertEqual(table.col_values(0), syllables_multiplicity[2][0])
        self.assertEqual(table.col_values(1), syllables_multiplicity[2][1])
        self.assertEqual(table.col_values(2), syllables_multiplicity[2][2])
        data = xlrd.open_workbook(file_path + 'number_of_length_of_syllables_with_repetition.xls')
        table = data.sheets()[0]
        self.assertEqual(table.col_values(0), number_of_length_of_syllables_with_repetition[2][0])
        self.assertEqual(table.col_values(1), number_of_length_of_syllables_with_repetition[2][1])
        data = xlrd.open_workbook(file_path + 'number_of_length_of_syllables_without_repetition.xls')
        table = data.sheets()[0]
        self.assertEqual(table.col_values(0), number_of_length_of_syllables_without_repetition[2][0])
        self.assertEqual(table.col_values(1), number_of_length_of_syllables_without_repetition[2][1])

    def test_4(self):
        module = TableModule(list_lengths_map[3], list_frequency_map[3], list_map_with_rep[3], list_map_wout_rep[3], file_path)
        module.run()
        time.sleep(1)
        data = xlrd.open_workbook(file_path + 'syllables_multiplicity.xls')
        table = data.sheets()[0]
        self.assertEqual(table.col_values(0), syllables_multiplicity[3][0])
        self.assertEqual(table.col_values(1), syllables_multiplicity[3][1])
        self.assertEqual(table.col_values(2), syllables_multiplicity[3][2])
        data = xlrd.open_workbook(file_path + 'number_of_length_of_syllables_with_repetition.xls')
        table = data.sheets()[0]        
        self.assertEqual(table.col_values(0), number_of_length_of_syllables_with_repetition[3][0])
        self.assertEqual(table.col_values(1), number_of_length_of_syllables_with_repetition[3][1])
        data = xlrd.open_workbook(file_path + 'number_of_length_of_syllables_without_repetition.xls')
        table = data.sheets()[0]
        self.assertEqual(table.col_values(0), number_of_length_of_syllables_without_repetition[3][0])
        self.assertEqual(table.col_values(1), number_of_length_of_syllables_without_repetition[3][1])

    def test_5(self):
        module = TableModule(list_lengths_map[4], list_frequency_map[4], list_map_with_rep[4], list_map_wout_rep[4], file_path)
        module.run()
        time.sleep(1)
        data = xlrd.open_workbook(file_path + 'syllables_multiplicity.xls')
        table = data.sheets()[0]
        self.assertEqual(table.col_values(0), syllables_multiplicity[4][0])
        self.assertEqual(table.col_values(1), syllables_multiplicity[4][1])
        self.assertEqual(table.col_values(2), syllables_multiplicity[4][2])
        data = xlrd.open_workbook(file_path + 'number_of_length_of_syllables_with_repetition.xls')
        table = data.sheets()[0]
        self.assertEqual(table.col_values(0), number_of_length_of_syllables_with_repetition[4][0])
        self.assertEqual(table.col_values(1), number_of_length_of_syllables_with_repetition[4][1])
        data = xlrd.open_workbook(file_path + 'number_of_length_of_syllables_without_repetition.xls')
        self.assertEqual(table.col_values(0), number_of_length_of_syllables_without_repetition[4][0])
        self.assertEqual(table.col_values(1), number_of_length_of_syllables_without_repetition[4][1])

if __name__ == '__main__':
    unittest.main()




