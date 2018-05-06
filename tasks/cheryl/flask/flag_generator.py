#!/usr/bin/python3

from random import seed, choice, shuffle
from string import ascii_letters, digits

ALPHA = ascii_letters + digits
NUMBER_OF_TEAMS = 500

def generate():
    for _ in range(NUMBER_OF_TEAMS):
        teamname = ''.join(choice(ALPHA) for _ in range(20))
        password = ''.join(choice(ALPHA) for _ in range(10))
        flag = 'QCTF{{Alb3r7_{}_B3rn4rd}}'.format(''.join(choice(ALPHA) for _ in range(10)))
        yield teamname, password, flag


if __name__ == "__main__":
    seed(0xd07abe57)
    data = list(generate())
    with open('teams_and_flags.py','w') as f:
        f.write('team_data = ' + str(data))