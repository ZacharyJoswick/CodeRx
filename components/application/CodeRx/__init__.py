from eventlet import monkey_patch as monkey_patch
monkey_patch()

import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_migrate import Migrate
from flask_mail import Mail


from CodeRx.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.debug = True

socketio= SocketIO(app, message_queue='redis://redis', async_mode='eventlet')

bootstrap = Bootstrap(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

mail = Mail(app)

# Setup Flask-Security
from CodeRx.models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from CodeRx import routes



