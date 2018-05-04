#!/usr/bin/python3

import os
import wave
import struct

from argparse import ArgumentParser
from itertools import cycle

from tokens import flags


def get_args():
    parser = ArgumentParser()
    parser.add_argument('--dir', help='output directory', required=True)
    parser.add_argument('--ratio', help='amplitude multiplier (default 0.002)', type=float, default=0.002)
    parser.add_argument('--container', help='container to hiding a flag inside', required=True)
    return parser.parse_args()


def load_wav_amps(path):
    with wave.open(path, 'rb') as wav:
        raw = wav.readframes(wav.getnframes())
        amps = []
        for i in range(0, len(raw), 2):
            amps.append(struct.unpack('<h', raw[i:i+2])[0])
        return amps


def save_stereo_wav(path, amps):
    raw = [struct.pack('<h', amp) for amp in amps]
    with wave.open(path, 'wb') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(8000)
        wav.writeframesraw(b''.join(raw))


def build_flag(flag):
    get_path = lambda symbol: 'speech/%s.wav' % symbol.lower()
    return sum(map(load_wav_amps, map(get_path, flag)), [])


def insert_flag(container, flag, ratio):
    result = []
    for c, f in zip(container, cycle(flag)):
        result += [c, c + int(f * ratio)]
    return result


if __name__ == '__main__':
    args = get_args()
    
    if not os.path.exists(args.dir):
        os.makedirs(args.dir)

    container = load_wav_amps(args.container)
    for token, flag in flags.items():
        print('Processing token %s' % token)
        result = insert_flag(container, build_flag(flag), args.ratio)
        save_stereo_wav('%s/%s.wav' % (args.dir, token), result)
