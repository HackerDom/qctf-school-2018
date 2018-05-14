#!/usr/bin/python3

import re

from flask import Flask, request, render_template, make_response, redirect, url_for

from tokens import flags


app = Flask(__name__)
app.config.update(dict(
    PREFERRED_URL_SCHEME = 'https'
))


@app.route('/')
def wrong_token():
    return 'Please, specify your team token.'


@app.route('/<token>/', methods=['GET', 'POST'])
def start(token):
    if request.cookies.get('reload'):
        url = url_for('start', token=token)
        response = make_response(render_template('reload.html', location=url))
        response.set_cookie('reload', '', expires=0)
        return response
    if token not in flags:
        return redirect(url_for('wrong_token'))
    flag = extract_flag_body(token)
    if request.method == 'GET':
        response = make_response(render_template('button.html'))
        response.set_cookie('index', '', expires=0)
        return response
    url = url_for('jump', token=token, symbol=flag[0])
    response = make_response(redirect(url))
    response.set_cookie('index', '0')
    return response


@app.route('/<token>/<symbol>/')
def jump(token, symbol=None):
    if token not in flags:
        return redirect(url_for('wrong_token'))
    flag = extract_flag_body(token)
    index = extract_index(request.cookies.get('index'))
    if not 0 <= index < len(flag) - 1:
        url = url_for('start', token=token)
        response = make_response(redirect(url))
        response.set_cookie('reload', 'true')
        response.set_cookie('index', '', expires=0)
        return response
    url = url_for('jump', token=token, symbol=flag[index + 1])
    response = make_response(redirect(url))
    response.set_cookie('index', str(index + 1))
    return response


def extract_index(cookie):
    try:
        return int(cookie)
    except:
        return -1


def extract_flag_body(token):
    return re.match('QCTF\{(\w+)+\}', flags[token]).group(1)


if __name__ == '__main__':
    app.run(threaded=True)
