import time
import os

import redis
from flask import url_for, send_from_directory, render_template, redirect
from flask_security import login_required, current_user, roles_required

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

@app.route('/editor')
@login_required
def editor():
    return render_template('editor.html', title='Editor')

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

@app.route('/403')
def error_403():
    return render_template('errors/403.html')
