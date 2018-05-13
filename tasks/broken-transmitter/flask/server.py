#!/usr/bin/python3

import time

from flask import Flask, request, render_template, redirect, url_for

from tokens import flags
from reader import Reader


app = Flask(__name__)
reader = Reader(
    filename='text.txt', 
    flag_length=len(list(flags.values())[0]), 
    step=16, 
    delay=15
)


@app.route('/')
def wrong_token():
    return 'Please, specify your team token.'


@app.route('/<token>/')
def show(token):
    if token not in flags:
        return redirect(url_for('wrong_token'))
    flag = flags[token]
    return render_template('show.html', message=reader.read(flag))


if __name__ == '__main__':
    app.run(threaded=True)
