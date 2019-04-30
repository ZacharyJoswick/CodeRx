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
    Submissions=[{"id":"vaognre","user_id":"Zackary Joswick","submission_date":"03-20-19","grade":75},
    {"id":"11iri33","user_id":"Jeffrey Smith","submission_date":"03-21-19","grade":33},
    {"id":"asdfrew","user_id":"Raj Patel","submission_date":"03-20-19","grade":30},
    {"id":"sadverw","user_id":"Marissa Bucaro","submission_date":"03-18-19","grade":70},]
    current_problems = [{"id":"asdfasdf","name":"HelloWorld", "class":"Brennaman Itec 120", "due_date":"01-28-19", "submissions":Submissions},
    {"id":"asdfasdf","name":"If", "class":"Brennaman Itec 120", "due_date":"02-05-19", "submissions":Submissions},
    {"id":"2verv","name":"Else", "class":"Brennaman Itec 120", "due_date":"02-10-19", "submissions":Submissions},
    {"id":"df3v","name":"If Else", "class":"Brennaman Itec 120", "due_date":"02-13-19", "submissions":Submissions},
    {"id":"q3rv ","name":"Money", "class":"Brennaman Itec 120", "due_date":"02-15-19", "submissions":Submissions},
    {"id":"asdfas","name":"Minutes", "class":"Brennaman Itec 120", "due_date":"02-31-19", "submissions":Submissions},
    {"id":"ghjk","name":"MovieTicket", "class":"Brennaman Itec 120", "due_date":"03-08-19", "submissions":Submissions},
    {"id":"2433ee","name":"For", "class":"Brennaman Itec 120", "due_date":"03-15-19", "submissions":Submissions},
    {"id":"scvas4","name":"vowelCount", "class":"Brennaman Itec 120", "due_date":"03-19-19", "submissions":Submissions},
    {"id":"qpdppp","name":"Reserse", "class":"Brennaman Itec 120", "due_date":"04-01-19", "submissions":Submissions},
    {"id":"awf432r","name":"Retrieve", "class":"Brennaman Itec 120", "due_date":"04-20-19", "submissions":Submissions},
    {"id":"43vbvwr","name":"Programming Assignment 4", "class":"Itec 324", "due_date":"04-29-19", "submissions":Submissions},
    {"id":"q234rq","name":"Iteration 3 Demo", "class":"Itec 370", "due_date":"04-30-19", "submissions":Submissions},]
    testCase = [{"input":"testvalue1"},{"input":"testvalue2"},{"input":"testvalue3"},{"input":"testvalue4"}]
    return render_template('editor.html', title='Editor', TestCases = testCase, current_problems=current_problems)

@app.route('/homepage')
@login_required
def homepage():
    Submissions=[{"id":"vaognre","user_id":"Zackary Joswick","submission_date":"03-20-19","grade":75},
    {"id":"11iri33","user_id":"Jeffrey Smith","submission_date":"03-21-19","grade":33},
    {"id":"asdfrew","user_id":"Raj Patel","submission_date":"03-20-19","grade":30},
    {"id":"sadverw","user_id":"Marissa Bucaro","submission_date":"03-18-19","grade":70},]
    current_problems = [{"id":"asdfasdf","name":"HelloWorld", "class":"Brennaman Itec 120", "due_date":"01-28-19", "submissions":Submissions},
    {"id":"asdfasdf","name":"If", "class":"Brennaman Itec 120", "due_date":"02-05-19", "submissions":Submissions},
    {"id":"2verv","name":"Else", "class":"Brennaman Itec 120", "due_date":"02-10-19", "submissions":Submissions},
    {"id":"df3v","name":"If Else", "class":"Brennaman Itec 120", "due_date":"02-13-19", "submissions":Submissions},
    {"id":"q3rv ","name":"Money", "class":"Brennaman Itec 120", "due_date":"02-15-19", "submissions":Submissions},
    {"id":"asdfas","name":"Minutes", "class":"Brennaman Itec 120", "due_date":"02-31-19", "submissions":Submissions},
    {"id":"ghjk","name":"MovieTicket", "class":"Brennaman Itec 120", "due_date":"03-08-19", "submissions":Submissions},
    {"id":"2433ee","name":"For", "class":"Brennaman Itec 120", "due_date":"03-15-19", "submissions":Submissions},
    {"id":"scvas4","name":"vowelCount", "class":"Brennaman Itec 120", "due_date":"03-19-19", "submissions":Submissions},
    {"id":"qpdppp","name":"Reserse", "class":"Brennaman Itec 120", "due_date":"04-01-19", "submissions":Submissions},
    {"id":"awf432r","name":"Retrieve", "class":"Brennaman Itec 120", "due_date":"04-20-19", "submissions":Submissions},
    {"id":"43vbvwr","name":"Programming Assignment 4", "class":"Itec 324", "due_date":"04-29-19", "submissions":Submissions},
    {"id":"q234rq","name":"Iteration 3 Demo", "class":"Itec 370", "due_date":"04-30-19", "submissions":Submissions},]
    past_problems = [{"name":"test", "class":"Brennaman Itec 120", "grade":75},
    {"name":"print", "class":"Dr. Chase Itec 220", "grade":100},
    {"name":"recursion", "class":"Dr. Chase Itec 220", "grade":75},]
    classes = [{"class_name":"Itec 120-01", "class_code":"4rfbsd", "Description":"8am MWF Java 1", "problems" : current_problems},
    {"class_name":"Itec 120-02", "class_code":"aR4bi3", "Description":"9am MWF Java 1", "problems" : current_problems},
    {"class_name":"Itec 120-03", "class_code":"ASFgtd", "Description":"10am MWF Java 1", "problems" : current_problems},
    {"class_name":"Itec 120-04", "class_code":"34tFSV", "Description":"11am TuThr Java 1", "problems" : current_problems},]
    return render_template('homepage.html', title='Homepage', email=current_user.email, 
    name=current_user.name, current_problems=current_problems, past_problems=past_problems, 
    classes=classes)#, problem_list = problem_list)

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
