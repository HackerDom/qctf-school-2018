#!/usr/bin/python3

import json

from flask import Flask, request, send_from_directory, render_template, redirect, url_for
from string import ascii_uppercase, ascii_lowercase, digits

from tokens import flags
from generator import generate_field


app = Flask(__name__)

FIELDS = dict() # use init_fields()
FLAG_SYMBOLS = ascii_uppercase + ascii_lowercase + digits + '{}_'


def init_fields():
    global FIELDS

    for symbol in FLAG_SYMBOLS:
        FIELDS[symbol] = generate_field(symbol)


@app.route('/')
def wrong_token():
    return 'Please, specify your team token.'


@app.route('/assets/<filename>')
def get_asset(filename):
    if filename in ['robot.js', 'styles.css']:
        return send_from_directory('assets', filename)
    return 'File not found.', 404


@app.route('/<token>/')
def robot(token):
    if token not in flags:
        return redirect(url_for('wrong_token'))
    return render_template('robot.html')


@app.route('/<token>/resolve/', methods=['POST'])
def resolve(token):
    if token not in flags:
        return redirect(url_for('wrong_token'))
    flag = flags[token]
    
    if not request.json:
        return dump_error('Please, use JSON!')
        
    level = parse_int(request.json.get('level'))
    if not isinstance(level, int):
        return dump_error('Please, send level number.')
    if not 0 <= level < len(flag):
        return dump_error('Incorrect level number!')

    field = FIELDS[flag[level]]

    x, y = parse_int(request.json.get('x')), parse_int(request.json.get('y'))
    if not isinstance(x, int) or not isinstance(y, int):
        return dump_error('Please, send robot coordinates.')
    if not 0 <= y < len(field) or not 0 <= x < len(field[0]):
        return dump_error('Incorrect robot coordinates!')

    return json.dumps(build_info(field, x, y))


def build_info(field, x, y):
    moves = dict()
    for move, dx, dy in [
        ('west', -1, 0), 
        ('northwest', -1, -1), 
        ('north', 0, -1), 
        ('northeast', 1, -1),
        ('east', 1, 0),
        ('southeast', 1, 1),
        ('south', 0, 1),
        ('southwest', -1, 1)
    ]:
        moves[move] = 0 <= y + dy < len(field) and \
                      0 <= x + dx < len(field[0]) and \
                      not field[y + dy][x + dx]
    return {
        'type': 'wall' if field[y][x] else 'empty',
        'moves': moves
    }


def parse_int(s):
    try:
        return int(s)
    except:
        return None


def dump_error(message):
    return json.dumps({'message': message}), 400


if __name__ == '__main__':
    init_fields()
    app.run(host='0.0.0.0', port=8080, threaded=True)
