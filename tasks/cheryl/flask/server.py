#!/usr/bin/python3

import logging
from flask import Flask, session, render_template, request, redirect
from database import init_db, check_user, get_task, update_answer, update_stage, get_user
from task_generator import generate
import os

app = Flask(__name__)
app.secret_key = b'\xd4\nUW\x93\xd6\x02,\x0c\xcc\xc0\xf6'
app.logger.setLevel(logging.DEBUG)
for handler in app.logger.handlers:
    handler.setLevel(logging.DEBUG)

@app.route("/")
def home():
    if session.get('logged_in', False):
        return redirect('/task')
    return render_template('login.html')


@app.route("/task", methods=['POST','GET'])
def task():
    if not session.get('logged_in', False):
        return redirect('/')
    
    team_id = session['team_id']
    if request.method == 'GET':
        stage = get_task(team_id).stage
        if stage > 10000:
            user = get_user(team_id)
            return user.flag
        else:
            answer, task_body = generate()
            update_answer(team_id, answer)
            return render_template('task.html', stage=stage, task=task_body)
    else:
        task = get_task(team_id)
        answer = str(request.form['answer'])
        if answer == task.answer:
            update_stage(team_id, task.stage + 1)
        return redirect('/task')

    
@app.route('/login', methods=['POST'])
def login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    res = check_user(POST_USERNAME, POST_PASSWORD)
    if res:
        session['logged_in'] = True
        session['team_id'] = res.id
    return redirect('/')

if __name__ == "__main__":
    app.run()