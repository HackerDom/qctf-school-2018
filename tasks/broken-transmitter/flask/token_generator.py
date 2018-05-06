#!/usr/bin/python3

import sys
import random

from string import ascii_uppercase, ascii_lowercase, digits
from hashlib import md5
from argparse import ArgumentParser
from Crypto.Util.number import bytes_to_long


ALPHABET = ascii_lowercase + ascii_uppercase + digits


def genstr(length, alpha):
    return ''.join([random.choice(alpha) for _ in range(length)])


def gentoken():
    return md5(genstr(random.randint(100, 200), ALPHABET).encode()).hexdigest()


parser = ArgumentParser()
parser.add_argument('--mask', help='flag mask (use %%s)', default='%s')
parser.add_argument('--seed', help='seed for a random generator (string)', required=True)
parser.add_argument('--count', help='teams count', type=int, default=1000)
parser.add_argument('--pretty', help='use \\n to separate tokens', action='store_true')
parser.add_argument('--length', help='random string length', type=int, default=5)
parser.add_argument('--alpha', help='alphabet to generate random string', default=ALPHABET)
args = parser.parse_args()

random.seed(bytes_to_long(args.seed.encode()))

tokens = dict()
while len(tokens) < args.count:
    s = genstr(args.length, args.alpha)
    if s in tokens.values():
        continue
    t = gentoken()
    if t in tokens:
        continue
    tokens[t] = args.mask % s

if args.pretty:
    print('flags = {')
    counter = 1
    for t, s in tokens.items():
        print('    \'%s\': \'%s\'' % (t, s) + (',' if counter < len(tokens) else ''))
        counter += 1
    print('}')
else:
    print(tokens)
