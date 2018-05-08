import subprocess
import sys

# Для генерации заданий необходим файл FILENAME в той же директории, что и генератор
# Запуск: python task_gen.py QCTF{**************************}
# На выходе зашифрованная строка из чисел с помощью скомпиленной в perl программы на chef

FILENAME = 'task.pl'

def send_flag_to_proc(proc, flag):
    assert len(flag) == 32

    for c in flag:
        proc.stdin.write((str(ord(c))).encode() + b'\n')
    
    print(proc.communicate()[0].decode())


if __name__ == '__main__':
    with subprocess.Popen(['perl', FILENAME], stdin=subprocess.PIPE, stdout=subprocess.PIPE) as proc:
        send_flag_to_proc(proc, sys.argv[1])