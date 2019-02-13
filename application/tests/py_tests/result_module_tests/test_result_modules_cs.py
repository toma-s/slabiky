from result_module import ResultModule
import unittest
import time

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

class TestStringMethods(unittest.TestCase):

    def test_1(self):
        module = ResultModule(list_lengths_map[0], list_frequency_map[0], "blabla/")
        module.run()
        time.sleep(1)
        self.assertEqual(module.map_with_rep, list_map_with_rep[0])
        self.assertEqual(module.map_wout_rep, list_map_wout_rep[0])

    def test_2(self):
        module = ResultModule(list_lengths_map[1], list_frequency_map[1], "blabla")
        module.run()
        time.sleep(1)
        self.assertEqual(module.map_with_rep, list_map_with_rep[1])
        self.assertEqual(module.map_wout_rep, list_map_wout_rep[1])

    def test_3(self):
        module = ResultModule(list_lengths_map[2], list_frequency_map[2], "blabla")
        module.run()
        time.sleep(1)
        self.assertEqual(module.map_with_rep, list_map_with_rep[2])
        self.assertEqual(module.map_wout_rep, list_map_wout_rep[2])

    def test_4(self):
        module = ResultModule(list_lengths_map[3], list_frequency_map[3], "blabla")
        module.run()
        time.sleep(1)
        self.assertEqual(module.map_with_rep, list_map_with_rep[3])
        self.assertEqual(module.map_wout_rep, list_map_wout_rep[3])

    def test_5(self):
        module = ResultModule(list_lengths_map[4], list_frequency_map[4], "blabla")
        module.run()
        time.sleep(1)
        self.assertEqual(module.map_with_rep, list_map_with_rep[4])
        self.assertEqual(module.map_wout_rep, list_map_wout_rep[4])

if __name__ == '__main__':
    unittest.main()




