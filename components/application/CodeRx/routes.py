import time
import os

import redis
from flask import url_for, send_from_directory, render_template
from flask_security import login_required

from CodeRx import app

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/editor')
@login_required
def editor():
    return render_template('editor.html', title='Editor')

@app.route('/login')
def login():
    return render_template('login.html', title='Login')