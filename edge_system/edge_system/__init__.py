from flask import Flask, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user
from functools import wraps
import os

app = Flask(__name__)

## Manejo de imagenes ....
ALLOWED_EXTENSIONS_FILE = set(['jpg','jpeg','gif','png'])
app.config['UPLOAD_FOLDER'] = os.path.realpath('.') + '/edge_system/static/uploads'

## Database configuration ... 
app.config.from_object('configuration.DevelopmentConfig')
db = SQLAlchemy(app)

## import views
from edge_system.machine.machine import machine
from edge_system.part.part import part

app.register_blueprint(machine)
app.register_blueprint(part)

## create the database
with app.app_context():
    db.create_all()