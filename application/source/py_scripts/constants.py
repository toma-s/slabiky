CONS = 0  #(except syllabic consonants)
SONOR = 1
VOWEL = 2
SPEC = 3  # special alphabet signs
SUBUNIT = 4  # letters make sound with letters they attach

PUNCT = 5
HYPHEN = 6


def get_conts(int):
    return eval(int)