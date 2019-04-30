import time
import os
import json
import requests

import redis
from flask import url_for, send_from_directory, render_template, redirect, request, make_response, jsonify, flash
from flask_security import login_required, current_user, roles_required
from flask_socketio import emit, send
from CodeRx import app, socketio

from CodeRx import app, db
from CodeRx.models import *

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

@app.route('/editor/<int:problem_id>')
@login_required
def editor_with_problem(problem_id):
    p=Problem.query.filter_by(id=problem_id).first()
    test_cases=[]
    for case in p.test_cases:
        test_cases.append({"id":case.id,"input":case.input,"expected_output":case.expected_output})
    tmpfile = p.files[0].content
    temp_problem={"description":p.description,"language":p.language,"id":p.id,"test_cases":test_cases, "name": p.name, "file_content": tmpfile}
    app.logger.info(temp_problem)
    return render_template('editor_single.html', title='Editor',problem=temp_problem)

@app.route('/new_problem', methods=['POST', 'GET'])
@login_required
def create_new_problem():
    if request.method == 'POST':
        if 'description' not in request.json.keys():
            return make_response(jsonify({'error': 'missing problem description'}), 400)
        if 'language' not in request.json.keys():
            return make_response(jsonify({'error': 'missing problem language'}), 400)
        if 'allowmultiplefiles' not in request.json.keys():
            return make_response(jsonify({'error': 'missing allowmultiplefiles'}), 400)
        if 'due_date' not in request.json.keys():
            return make_response(jsonify({'error': 'missing due date'}), 400)
        if 'test_cases' not in request.json.keys():
            return make_response(jsonify({'error': 'missing test cases'}), 400)
        app.logger.info(request.json)
        return make_response(jsonify({'response': 'success'}), 200)
    else:
        return render_template('create_problem.html', title='Create Problem')

@app.route('/editor')
@login_required
def editor():
    testCase = [{"input":"testvalue1"},{"input":"testvalue2"},{"input":"testvalue3"},{"input":"testvalue4"}]
    return render_template('editor.html', title='Editor', TestCases = testCase)

@app.route('/join_class')
@login_required
def join_class():
    return render_template('join_class.html', title='Join Class')

@app.route('/join_class_code', methods=['POST'])
@login_required
def join_class_code():
    code = request.form.get("classJoinCode")
    app.logger.info(f"User: {current_user.email} attempted to join class with code: {code}")
    the_class = Class.query.filter_by(join_code=code).first()
    if the_class is not None:
        current_user.classes.append(the_class)
        flash('You have successfully joined the class')
    else:
        flash('Error, Invalid code')
    
    return render_template('join_class.html', title='Join Class')

@app.route('/create_professor', methods=['POST'])
@login_required
@roles_required('admin')
def create_professor():
    name = request.form.get("name")
    email = request.form.get("email")
    
    professor_role = Role.query.filter_by(name="professor").first()
    student_role = Role.query.filter_by(name="student").first()

    new_user = User(name=name, email=email)
    if student_role in new_user.roles:
        new_user.roles.remove(student_role)
    new_user.roles.append(professor_role)

    db.session.add(new_user)
    db.session.commit()
    
    flash('Professor Successfully Created')
    
    return redirect("/admin", 200)

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

#displying problems on homepage
#@app.route('/homepage/<int:user.id>')
#@login_required
#def homepage()
#    p=problem.query.filter_by(id='user.id').all()
#    problem=[]
#    for problem in p.problem_id:
#        problem.append({"id":problem.id,"name":problem.name})
#    problem_id = {"id":p.id, "name":p.name}
#    return render_template('homepage.html', title='Homepage')

@app.route('/class_management')
# @roles_required('admin')
@login_required
def class_management():
    return render_template('class_management.html', title='Class Management')

@app.route('/admin')
@login_required
@roles_required('admin')
def admin():
    student_role = Role.query.filter_by(name="student").first()
    students = User.query.filter(User.roles.any(Role.id.in_([student_role.id]))).all()
    ret_students = []
    for student in students:
        ret_students.append({"name":student.name, "email": student.email})

    professor_role = Role.query.filter_by(name="professor").first()
    professors = User.query.filter(User.roles.any(Role.id.in_([professor_role.id]))).all()
    ret_professors = []
    for professor in professors:
        ret_professors.append({"name":professor.name, "email": professor.email})
    app.logger.info(f"Found professors: {ret_professors}")
    return render_template('admin_page.html', title='Administrator Tools', students=ret_students, professors=ret_professors)

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

@socketio.on('new_problem_from_professor')
def new_problem_from_professor(message):
    app.logger.info(message)

    problem = message["problem"]

    problem["callback_address"] = "http://web:5000/job_complete"
    problem["compile_timeout"] = 5
    problem["run_timeout"] = 5
    problem["other"] = {}

    app.logger.info(problem)

    r = requests.post(url="http://api:4520/api/1.0/new_job", json=problem, timeout=4)
    app.logger.debug(f'Callback url resulted in a response code of: {r.status_code}')

@socketio.on('professor_start_editing')
def professor_start_editing(message):
    app.logger.info(message)

    if current_user.last_problem_id == None:
        tmpProb = Problem()
        db.session.add(tmpProb)
        db.session.commit()

        current_user.last_problem_id = tmpProb.id
        db.session.commit()

        socketio.emit("new_problem_id", tmpProb.id)
    else:
        socketio.emit("new_problem_id", current_user.last_problem_id)
        tmpProb = Problem.query.filter_by(id=current_user.last_problem_id).first()

        if len(tmpProb.files) > 0:
            file_contents = tmpProb.files[0].content
        else:
            file_contents = ""

        test_cases = []

        if len(tmpProb.test_cases) > 0:
            for case in tmpProb.test_cases:
                test_cases.append({"input": case.input, "expected_output": case.expected_output})

        prob = {'title': tmpProb.name, "description": tmpProb.description, 
                'file_contents': file_contents, "test_cases": test_cases}
                
        socketio.emit("reload_problem", prob)


@socketio.on('professor_save_problem')
def professor_save_problem(message):
    app.logger.info(message)

    problem = message["problem"]

    tmpProb = Problem.query.filter_by(id=problem["id"]).first()
    tmpProb.description = problem["description"]
    tmpProb.name = problem["title"]
    tmpProb.language = "java"
    tmpProb.allowmultiplefiles = False
    tmpProb.entry_command = problem["run_file"]
    db.session.commit()
    
    if len(tmpProb.files ) == 0:
        app.logger.info("Adding file")
        tmpFile = Problem_Base_File(file_name=problem["files"][0]["filename"], 
                                    content=problem["files"][0]["contents"])
        
        tmpProb.files.append(tmpFile)
        db.session.add(tmpFile)

        db.session.commit()
    else:
        app.logger.info("Using an existing file")
        tmpProb.files[0].file_name = problem["files"][0]["filename"]
        tmpProb.files[0].content = problem["files"][0]["contents"]
        db.session.commit()


    db.session.commit()
    if len(tmpProb.test_cases) == len(problem["test_cases"]):
        for i in range(0, len(problem["test_cases"])):
            tmpProb.test_cases[i].input = problem["test_cases"][i]["input"]
            tmpProb.test_cases[i].expected_output = problem["test_cases"][i]["expected_output"]
    elif len(tmpProb.test_cases) == 0:
        for i in range(0, len(problem["test_cases"])):
            tempCase = TestCase(input=problem["test_cases"][i]["input"], expected_output=problem["test_cases"][i]["expected_output"])
            tmpProb.test_cases.append(tempCase)
            db.session.add(tempCase)
            db.session.commit()
    else:
        for case in tmpProb.test_cases:
            tmpProb.test_cases.remove(case)
        
        for i in range(0, len(problem["test_cases"])):
            tempCase = TestCase(input=problem["test_cases"][i]["input"], expected_output=problem["test_cases"][i]["expected_output"])
            tmpProb.test_cases.append(tempCase)
            db.session.add(tempCase)
            db.session.commit()


    # app.logger.info(tmpProb.created_date)

    # problem["callback_address"] = "http://web:5000/job_complete"
    # problem["compile_timeout"] = 5
    # problem["run_timeout"] = 5
    # problem["other"] = {}

    # app.logger.info(problem)

    # r = requests.post(url="http://api:4520/api/1.0/new_job", json=problem, timeout=4)
    # app.logger.debug(f'Callback url resulted in a response code of: {r.status_code}')

