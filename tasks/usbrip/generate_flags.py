import random
import argparse
import string
import json

ALPHABET=string.ascii_letters+string.digits
FLAG_PREFIX='QCTF{s0_uSB_'

def parse_args():
    parser = argparse.ArgumentParser(prog='generate_flags.py', description='Generates flags for teams')
    parser.add_argument('count', type=int, help='Teams number')
    parser.add_argument('seed', type=int, help='Random generator seed')
    parser.add_argument('id_length', type=int, nargs='?', help='Team id length. Default is 8', default=8)
    return parser.parse_args()

def generate_string(length):
    return ''.join([random.choice(ALPHABET) for _ in range(length)])

def main():
    args=parse_args()
    flags=[]
    random.seed(args.seed)
    while len(flags)<args.count:
        team_id=generate_string(args.id_length)
        suffix=generate_string(8)
        flag=FLAG_PREFIX+suffix+'}'
        if len(list(filter(lambda tup: team_id == tup[0] or flag == tup[1], flags))) == 0:
            flags.append((team_id, flag))

        with open('flags.json', 'w') as file:
            json.dump(flags, file, indent=4)

if __name__ == '__main__':
    main()