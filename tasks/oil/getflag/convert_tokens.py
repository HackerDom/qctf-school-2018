#!/usr/bin/python3

from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser()
    parser.add_argument('--tokens', help='path to tokens file', required=True)
    parser.add_argument('--output', help='path to output file', required=True)
    return parser.parse_args()


def convert(tokens):
    result = ''
    
    for token, flag in tokens.items():
        result += '%s %s\n' % (token, flag)

    return result


if __name__ == '__main__':
    args = get_args()

    with open(args.tokens, 'r') as file:
        exec(file.read())

    with open(args.output, 'w') as file:
        file.write(convert(flags))
