#!/usr/bin/python3

from random import seed, choice, shuffle
from string import ascii_letters, digits
import subprocess
import os
import shutil

ALPHA = list(ascii_letters + digits)
NUMBER_OF_TEAMS = 500
DIRNAME = "tasks"
PERM = (0,0,1,2,3,1,0,0,1,4)

def generate():
    for _ in range(NUMBER_OF_TEAMS):
        shuffle(ALPHA)
        team = ''.join(choice(ALPHA) for _ in range(20))
        flag = ''.join(map(lambda x: ALPHA[x], PERM))
        yield team, flag

def create_task(team, flag, task_content):
    arr = [0] * 256
    
    alpha = []
    for x in flag:
        if x not in alpha:
            alpha.append(x)
    for i, x in enumerate(alpha):
        arr[(ord(x))] = i+1
    
    os.makedirs(os.path.join(DIRNAME, team))

    with open(os.path.join(DIRNAME, team, 'task.s'), 'w') as f:
        f.write(task_content.replace('placeholder', ','.join(map(str, arr))))
    subprocess.call([os.path.join(os.curdir,'compile.sh'), os.path.join(DIRNAME, team, 'task')])
    os.remove(os.path.join(DIRNAME, team, 'task.s'))

if __name__ == "__main__":
    seed(0xdeaddaed)

    if os.path.exists(DIRNAME):
        shutil.rmtree(DIRNAME, ignore_errors=True)
    os.makedirs(DIRNAME)

    with open('task.s','r') as f:
        task_content = f.read()

    data = []
    for x in generate():
        create_task(*x, task_content)
        data.append(x)
    
    with open('teams_and_flags.py','w') as f:
        f.write(str(data))