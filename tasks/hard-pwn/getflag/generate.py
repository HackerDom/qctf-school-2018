#!/usr/bin/python3

import re
import sys

from argparse import ArgumentParser


TEMPLATE = 'getflag.template'
TOKENS   = 'tokens'
OUTPUT   = 'getflag.c'


DEFINES = '''
#define TOKENS_FILENAME "{}"
#define TOKEN_LENGTH    {}
#define FLAG_LENGTH     {}
'''


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: ./generate.py <path-to-tokens>')
        sys.exit(1)
    
    tokens_path = sys.argv[1]

    with open(TEMPLATE, 'r') as file:
        template = file.read()

    with open(TOKENS, 'r') as file:
        line = file.readline()

    match = re.match('(\S+) (\S+)\n', line)
    assert match, 'Invalid tokens format!'
    token_length = len(match.group(1))
    flag_length = len(match.group(2))

    with open(OUTPUT, 'w') as file:
        file.write(template.replace('%%%INSERT_DEFINES_HERE%%%', DEFINES.format(tokens_path, token_length, flag_length)))