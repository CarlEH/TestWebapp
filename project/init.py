from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import flask_sqlalchemy
from flask_wtf.csrf import CSRFProtect

import config
import logging

# def create_app():
flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONN_URI
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.config['SECRET_KEY'] = config.SECRET_KEY
flask_app.app_context().push()

csrf = CSRFProtect(flask_app)
bcrypt = Bcrypt(flask_app)
login_manager = LoginManager(flask_app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from models import db
db.init_app(flask_app)
db.create_all()

import logging

app = Flask(__name__)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
# flask_app.logger.handlers.extend(gunicorn_error_logger.handlers)
flask_app.logger.setLevel(logging.DEBUG)
flask_app.logger.info('this will show in the log')

# return flask_app, bcrypt, db, login_manager
