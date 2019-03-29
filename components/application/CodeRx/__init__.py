from eventlet import monkey_patch as monkey_patch
monkey_patch()

import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
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

from CodeRx import routes, models