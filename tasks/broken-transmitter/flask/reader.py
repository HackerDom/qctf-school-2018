#!/usr/bin/python3

from time import time


def hex_wrapper(func):
    hexcode = lambda symbol: hex(ord(symbol))[2:].zfill(2)

    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        return ' '.join(map(hexcode, result))
    
    return inner


class Reader:

    def __init__(self, filename, flag_length, step, delay):
        with open(filename, 'r') as file:
            self._text = file.read()

        assert (len(self._text) + flag_length) % step == 0

        self._step = step
        self._delay = delay

        self._index = 0
        self._previous = time()


    @hex_wrapper
    def read(self, flag):
        if time() - self._previous > self._delay:
            self._index += self._step

        if 0 <= self._index - len(self._text) < len(flag):
            flag_index = self._index - len(self._text)
            return flag[flag_index:flag_index+self._step]
        
        if self._index > len(self._text) + len(flag):
            self._index = 0
        
        self._previous = time()

        return self._text[self._index:self._index + self._step]
