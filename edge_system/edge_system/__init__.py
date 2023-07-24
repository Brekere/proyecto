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

# manejo de logoin .... 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "fauth.login"

def rol_admin_need(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if current_user.id_role.value != 'Administrador':
            flash('Acceso solo a administrador','danger')
            return redirect(url_for('fauth.login'))
        return f(*args, **kwds)
    return wrapper

## import views
from edge_system.machine.machine import machine
from edge_system.part.part import part
from edge_system.production.production import production
from edge_system.fauth.users import fauth
from edge_system.control.control import control
from edge_system.home.home import home

app.register_blueprint(machine)
app.register_blueprint(part)
app.register_blueprint(production)
app.register_blueprint(fauth)
app.register_blueprint(control)
app.register_blueprint(home)

## create the database
with app.app_context():
    db.create_all()