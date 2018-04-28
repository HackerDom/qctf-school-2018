#!/usr/bin/python3

import sys
import random

from string import ascii_uppercase, ascii_lowercase, digits
from hashlib import md5
from argparse import ArgumentParser
from Crypto.Util.number import bytes_to_long


secret = 'pleAsed0ntgue$$_'
alpha = ascii_lowercase + ascii_uppercase + digits


def genstr(length):
    return ''.join([random.choice(alpha) for _ in range(length)])


def gentoken(str):
    return md5((secret + str + secret).encode()).hexdigest()


parser = ArgumentParser()
parser.add_argument('--mask', help='flag mask (use %%s)', type=str, default='%s')
parser.add_argument('--seed', help='seed for a random generator (string)', type=str, required=True)
parser.add_argument('--count', help='teams count', type=int, default=1000)
parser.add_argument('--pretty', help='use \\n to separate tokens', action='store_true')
parser.add_argument('--length', help='random string length', type=int, default=5)
args = parser.parse_args()

random.seed(bytes_to_long(args.seed.encode()))

tokens = dict()
while len(tokens) < args.count:
    s = genstr(args.length)
    if s in tokens.values():
        continue
    t = gentoken(s)
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
