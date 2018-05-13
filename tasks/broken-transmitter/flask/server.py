#!/usr/bin/python3

from time import time

from flask import Flask, request, render_template, redirect, url_for

from tokens import flags


app = Flask(__name__)

TOKENS = dict()
PART_LENGTH = 16
DELAY = 5
TEXT = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.   '''



def tohex(text):
    hexcode = lambda symbol: hex(ord(symbol))[2:].zfill(2)
    ' '.join(map(hexcode, result))
    

@app.route('/')
def wrong_token():
    return 'Please, specify your team token.'


@app.route('/<token>/')
def show(token):
    global TOKENS
    flag = flags[token]
    message = TEXT + flag

    if token not in flags:
        return redirect(url_for('wrong_token'))
    if token not in TOKENS:
        TOKENS[token] = (time(), 0)
    elif time() - TOKENS[token][0] > DELAY:
        TOKENS[token] = (time(), TOKENS[token][1] + PART_LENGTH)
    if TOKENS[token][1] + PART_LENGTH > len(message):
        TOKENS[token] = (time(), 0)

    return render_template('show.html', message=tohex(message[TOKENS[token][1]:TOKENS[token][1] + PART_LENGTH]))


if __name__ == '__main__':
    app.run(threaded=True)
