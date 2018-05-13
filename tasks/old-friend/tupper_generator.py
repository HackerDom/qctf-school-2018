#!/usr/bin/python3

import os

from argparse import ArgumentParser

from tokens import flags
from pictures import pictures


def make_field(text):
    width, height = 106, 17
    field = [[0 for y in range(height)] for x in range(width)]
    offset = 4
    
    assert width > len(text) * offset

    for index, char in enumerate(text):
        picture = pictures[char]
        for y in range(len(picture)):
            for x in range(len(picture[y])):
                field[1 + offset * index + x][1 + y] = picture[y][x]

    return field
    

def make_number(text):
    field = make_field(text)
    number = ''

    for x in range(len(field)):
        for y in range(len(field[x])):
            bit = field[x][-y - 1]
            number += str(bit)

    return int(number[::-1] , 2) * 17


def write_number(number, path):
    with open(path, 'w') as file:
        file.write(str(number) + '\n')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--dir', help='output directory', required=True)
    parser.add_argument('--folders', help='save files to differens folders', action='store_true')
    args = parser.parse_args()

    if not os.path.exists(args.dir):
        os.makedirs(args.dir)

    if args.folders:
        path = '%s/%%s/number.txt' % args.dir
    else:
        path = '%s/%%s.txt' % args.dir

    for token, flag in flags.items():
        print('Processing token: %s' % token)
        number = make_number(flag)
        if args.folders:
            os.makedirs('%s/%s' % (args.dir, token))
        write_number(number, path % token)
