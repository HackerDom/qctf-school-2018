import os
import sys
import random

from hashlib    import sha1
from subprocess import call
from shutil     import copyfile, copy2


TOKENS_PATH = '/tmp/hard-pwn/tokens'


TASK_NAME   = 'hard-pwn'
SEED        = 0x6b6f6e617461
FLAG_NUMBER = 500
MAX_NUMBER  = 1e10


FLAG_PREFIX = 'QCTF{y0u_4r3_7h3_G0D_0f_R0P_'

FLAG_SIZE  = 50
TOKEN_SIZE = 40

TASKS_DEPLOY = '../../tasks-deploy/hard-pwn/'


def gen_string(size=40):
    if size > 40:
        print('[-] Bad size, try less or equal to 40')
        sys.exit(1)
    
    a = sha1(str(random.randint(1, MAX_NUMBER)).encode()).hexdigest()
    b = sha1(str(random.randint(1, MAX_NUMBER)).encode()).hexdigest()
    half = len(a) // 2

    return (b[:half] + a[half:])[:size]


def gen_check(flags):
    TEMPLATE = '''
def check(attempt, context):
    if attempt.answer == flags[attempt.participant.id % len(flags)]:
            return Checked(True)
    if attempt.answer in flags:
            return CheckedPlagiarist(False, flags.index(attempt.answer))
    return Checked(False)
'''
    check_code = 'flags = [{}]\n\n'.format(', '.join(['"{}"'.format(flag) for flag in flags])) + TEMPLATE

    with open(os.path.join(TASKS_DEPLOY, 'check.py'), 'w') as f:
        f.write(check_code)


def gen_generate(tokens):
    TEMPLATE = '''
TITLE = "Проблема мутантов"
STATEMENT_TEMPLATE = \'\'\'
## Проблема мутантов

Ах, я чуть не забыл рассказать самое интересное!

Вы слышали, что неделю назад у нас появился отдел исследований? Мы назвали его **Research & Obsession & Persistence**.

Название говорит само за себя, но я всё же объясню, чем он занимается. Если кратко, то они ловят мутантов и отправляют в лаборатории для дальнейшего изучения. За эту неделю отдел смог оценить влияние радиации на сам процесс мутирования и выявить зависимость между дозой излучения и скоростью формирования новых генов.

Пришлось ещё подумать над тем, как ловить сами объекты исследований. Ребята из отдела ROP не смогли придумать ничего лучше, чем связывать мутантов верёвками и транспортировать их с помощью канатов. Не лучшая идея, но по-другому придумать сложно: мутанты сопротивляются и могут начать атаковать.

За неделю было поймано столько мутантов, что у нас полностью закончились верёвки и почти не осталось канатов. Вам нужно спуститься в убежище и принести оттуда столько, сколько сможете. Не забывайте, что на входе вам придётся подтвердить личность.

Вы же помните свои данные?

Чтобы получить флаг, нужно запустить **getflag** и передать ему токен первым аргументом.
Ваш токен: `{0}`
Пример: `./getflag {0}`
[auth](/static/files/<task.id>/auth)
[libc.c](/static/files/<task.id>/libc.so.6)
\'\'\'

def generate(context):
    participant = context['participant']
    token = tokens[participant.id % len(tokens)]
    return TaskStatement(TITLE, STATEMENT_TEMPLATE.format(token))
'''
    generate_code = 'tokens = [{}]\n\n'.format(', '.join(['"{}"'.format(token) for token in tokens])) + TEMPLATE

    with open(os.path.join(TASKS_DEPLOY, 'generate.py'), 'w') as f:
        f.write(generate_code)


def configure_getflag(tokens, flags):
    os.chdir('./getflag')

    with open('tokens', 'w') as fp:
        for token, flag in zip(tokens, flags):
            fp.write('{} {}\n'.format(token, flag))
    
    print('[~] Creating {} path...'.format(TOKENS_PATH))
    if not os.path.exists(os.path.dirname(TOKENS_PATH)):
        try:
            os.makedirs(os.path.dirname(TOKENS_PATH))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    copyfile('./tokens', TOKENS_PATH)
    call(['./compile.sh', TOKENS_PATH])

    os.chdir('../')


def generate_tokens_flags():
    tokens = []
    flags  = []

    os.chdir('./getflag')

    random.seed(SEED)
    for _ in range(FLAG_NUMBER):
        token = gen_string(TOKEN_SIZE)
        flag  = FLAG_PREFIX + gen_string(FLAG_SIZE - len(FLAG_PREFIX) - 1) + '}'
        
        tokens.append(token)
        flags.append(flag)
    os.chdir('../')
    return tokens, flags


def build_service():
    os.chdir('./service')
    call(['./compile.sh'])
    os.chdir('../')


def main():
    print('[*] Configuration is starting...')
    
    print('\n[~] Building the service...')
    build_service()
    print('[+] Done')

    print('\n[~] Generating flags and tokens...')
    tokens, flags = generate_tokens_flags()
    print('Tokens: [{}, ..., {}]'.format(tokens[0], tokens[-1]))
    print('Flags:  [{}, ..., {}]'.format(flags[0], flags[-1]))
    print('[+] Done')

    print('\n[~] Configuring getflag and creating tokens file...')
    configure_getflag(tokens, flags)
    print('[+] Done')

    print('\n[~] Generating check.py')
    gen_check(flags)
    print('[+] Done')

    print('\n[~] Generating generate.py')
    gen_generate(tokens)
    print('[+] Done')

    print('\n\n[+] Everything is built and configured!\nNow see README.md file to see what to do next.')
    


if __name__ == '__main__':
    main()