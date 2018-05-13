from string import digits, ascii_letters
from random import seed, choice
import subprocess
import re


def generate(teams_count):
    seed(37428)
    ALPHA = digits + ascii_letters
    NUMBER_OF_TEAMS = teams_count

    tokens_and_flags = {}
    tokens = []
    flags = []
    for i in range(NUMBER_OF_TEAMS):
        token = ''.join(choice(ALPHA) for _ in range(32)).upper()
        tokens.append(token)
        proc = subprocess.Popen(['./patched', token], stdout=subprocess.PIPE)
        output_with_flag = str(proc.communicate()[0], encoding='utf-8')
        flag = re.search('(?<=generated!\n)(.*)', output_with_flag).group(1)
        flags.append(flag)
        tokens_and_flags[token] = flag

    # print(tokens_and_flags)
    # print(tokens)
    # print(flags)

    return tokens


if __name__ == '__main__':
    generate(500)
