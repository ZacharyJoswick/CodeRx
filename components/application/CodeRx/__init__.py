from eventlet import monkey_patch as monkey_patch
monkey_patch()

import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, user_registered
from flask_migrate import Migrate
from flask_mail import Mail


from CodeRx.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
app.debug = True

socketio= SocketIO(app, message_queue='redis://redis', async_mode='eventlet')

bootstrap = Bootstrap(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

mail = Mail(app)

# Setup Flask-Security
from CodeRx.models import User, Role, Problem, Submitted, files, testcase, test_case_results
user_datastore = SQLAlchemyUserDatastore(db, User, Role, Problem, Submitted, files, testcase, test_case_results)
security = Security(app, user_datastore)

@app.before_first_request
def create_user():
    db.create_all()
    user_datastore.find_or_create_role(name="admin")
    user_datastore.find_or_create_role(name="professor")
    user_datastore.find_or_create_role(name="student")
    db.session.commit()

@user_registered.connect_via(app)
def user_registered_sighandler(app, user, confirm_token):
    default_role = user_datastore.find_role("student")
    user_datastore.add_role_to_user(user, default_role)
    db.session.commit()

from CodeRx import routes
