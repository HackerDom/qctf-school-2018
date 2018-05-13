#!/usr/bin/python3

import re

from argparse import ArgumentParser


TEXT = '''
#define TOKEN_LENGTH %d
#define FLAG_LENGTH %d
'''


def get_args():
    parser = ArgumentParser()
    parser.add_argument('--template', help='path to getflag.c.template', required=True)
    parser.add_argument('--tokens', help='path to file with tokens', required=True)
    parser.add_argument('--output', help='path to getflag.c', required=True)
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    with open(args.template, 'r') as file:
        template = file.read()

    with open(args.tokens, 'r') as file:
        line = file.readline()

    match = re.match('(\S+) (\S+)\n', line)
    assert match, 'Invalid tokens format!'
    token_length = len(match.group(1))
    flag_length = len(match.group(2))

    with open(args.output, 'w') as file:
        file.write(template.replace('%%%INSERT_DEFINES_HERE%%%', TEXT % (
            token_length,
            flag_length
        )))
