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
    temp_problem={"description":p.description,"language":p.language,"id":p.id,"test_cases":test_cases}
    return render_template('editor.html', title='Editor',problem=temp_problem)

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
    app.logger.info(f"Current User Information: {current_user.email}")
    #User.query.filter_by(email=current_user.email)
    # new_sumbission = Submission(files="A file")
    # db.session.add(new_sumbission)
    # db.session.commit()
    #tmp = Submission.query.filter_by(id=1).first()
    #app.logger.info(f"Query Result: {tmp.files}")
    return render_template('homepage.html', title='Homepage')

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
