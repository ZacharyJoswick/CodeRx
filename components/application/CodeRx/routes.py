import time
import os
import json
import requests

import redis
from flask import url_for, send_from_directory, render_template, redirect, request, make_response, jsonify
from flask_security import login_required, current_user, roles_required
from flask_socketio import emit, send
from CodeRx import app, socketio

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect("/homepage", code=302)
    else:
        return render_template('index.html')

@app.route('/editor')
@login_required
def editor():
    testCase = [{"input":"testvalue1"},{"input":"testvalue2"},{"input":"testvalue3"},{"input":"testvalue4"}]
    return render_template('editor.html', title='Editor', TestCases = testCase)

@app.route('/homepage')
@login_required
def homepage():
    current_problems = [{"name":"HelloWorld", "class":"Brennaman Itec 120", "due_date":"01-28-19"},
    {"name":"If", "class":"Brennaman Itec 120", "due_date":"02-05-19"},
    {"name":"Else", "class":"Brennaman Itec 120", "due_date":"02-10-19"},
    {"name":"If Else", "class":"Brennaman Itec 120", "due_date":"02-13-19"},
    {"name":"Money", "class":"Brennaman Itec 120", "due_date":"02-15-19"},
    {"name":"Minutes", "class":"Brennaman Itec 120", "due_date":"02-31-19"},
    {"name":"MovieTicket", "class":"Brennaman Itec 120", "due_date":"03-08-19"},
    {"name":"For", "class":"Brennaman Itec 120", "due_date":"03-15-19"},
    {"name":"vowelCount", "class":"Brennaman Itec 120", "due_date":"03-19-19"},
    {"name":"Reserse", "class":"Brennaman Itec 120", "due_date":"04-01-19"},
    {"name":"Retrieve", "class":"Brennaman Itec 120", "due_date":"04-20-19"},
    {"name":"Programming Assignment 4", "class":"Itec 324", "due_date":"04-29-19"},
    {"name":"Iteration 3 Demo", "class":"Itec 370", "due_date":"04-30-19"},]
    past_problems = [{"name":"test", "class":"Brennaman Itec 120", "grade":75},
    {"name":"print", "class":"Dr. Chase Itec 220", "grade":100},
    {"name":"recursion", "class":"Dr. Chase Itec 220", "grade":75},]
    return render_template('homepage.html', title='Homepage', email=current_user.email, name=current_user.name, current_problems=current_problems, past_problems=past_problems)#, problem_list = problem_list)

@app.route('/class_management')
# @roles_required('admin')
@login_required
def class_management():
    return render_template('class_management.html', title='Class Management')

@app.route('/admin')
@login_required
@roles_required('admin')
def admin():
    return render_template('admin_page.html', title='Administrator Tools')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Edit Profile')

@app.route('/single_problem')
@login_required
def single_problem():
    return render_template('view_single_problem.html', title='View Problem')

@app.route('/user_submissions')
@login_required
def user_submissions():
    return render_template('view_user_submissions.html', title='All User Submissions')

@app.route('/terminal')
def terminal():
    return render_template('terminal.html')

@app.route('/403')
def error_403():
    return render_template('errors/403.html')

@app.route('/job_complete', methods=['POST'])
def job_complete():
    app.logger.info(request.json)
    socketio.emit("problem_result",request.json["run"])
    return make_response(jsonify({'result': 'job completed successfully'}), 200)

@socketio.on('new_problem_from_user')
def test_message(message):
    app.logger.info(message)

    problem = {}

    with open('./CodeRx/test.json') as json_file:  
        problem = json.load(json_file)

    problem["files"][0]["contents"] = message["data"]

    r = requests.post(url="http://api:4520/api/1.0/new_job", json=problem, timeout=4)
    app.logger.debug(f'Callback url resulted in a response code of: {r.status_code}')

    # app.logger.info(problem["files"][0]["contents"])

    # emit('my response', {'data': 'got it!'})  
