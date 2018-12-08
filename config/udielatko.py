import sys


def upper(input):
    for x in input:
        if x != '\n':
            print('\"{}\"'.format(x[0]), end=', ')


def lower1(input):
    for x in input:
        if x != '\n':
            if x[-1] == '\n':
                x = x[:-1]
            print('\"{}\"'.format(x.split(' ')[1]), end=', ')


def lower(input): # input: "1", "2", "3"... "n"
    print('{')
    for letter in input[0].split():
        print(letter.replace(',','') + ': "",', end=' ')
    print('}')


def get_single(input):
    for x in input[0].split(' '):
        if x[-1] == '\n':
            x = x[:-1]
        print('\"{}\"'.format(x), end=', ')


def lower_upd(input):
    for x in input[0].split(','):
        letter, sign = x.split(':')
        print(letter.strip() + ': { "phoneme-length": 1, "sign": ' + sign.strip() + "},")

def quot(input):
    for line in input:
        for word in line.split(' '):
            print('"{}",'.format(word), end=' ')


if __name__ == '__main__':
    # upper(list(sys.stdin))
    # lower1(list(sys.stdin))
    # lower(list(sys.stdin))
##    get_single(list(sys.stdin))
    # lower_upd(list(sys.stdin))
    quot(list(sys.stdin))
