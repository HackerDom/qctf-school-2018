#!/usr/bin/python3

import re

from flask import Flask, render_template, send_from_directory, redirect, url_for
from argparse import ArgumentParser

from tokens import flags


app = Flask(__name__)


@app.route('/')
def wrong_token():
    return 'Please, specify your team token.'


@app.route('/<token>/')
def observe(token):
    if token not in flags:
        return redirect(url_for('wrong_token'))
    flag = flags[token]
    return render_template('index.html', secret=encode_flag(flag))


@app.route('/assets/<filename>')
def get_asset(filename):
    if filename in ['chat.js', 'styles.css']:
        return send_from_directory('assets', filename)
    return 'File not found', 404


def encode_flag(flag):
    msg = 'vvr!73 7h3 ffL46'
    cipher = '\x1b'.join(list(msg))
    assert len(flag) == len(cipher)
    secret = [ord(c) ^ (ord(f) + 1) for c, f in zip(cipher, flag[::-1])]
    return repr(secret[::-1])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--port', required=True, type=int)
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port, threaded=True)
