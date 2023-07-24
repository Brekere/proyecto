from flask import Blueprint, render_template
import numpy as np
from flask_login import login_required

control = Blueprint('control', __name__)

@control.before_request
@login_required
def constructor():
   pass

@control.route('/panel')
def panel():
    '''print('Panel')'''
    return render_template('control/panel.html')
    
@control.route('/panel/stop')
def stop():
    '''print('stop')
    flash('Paro de emergencia','danger')'''
    return render_template('control/panel.html')    

@control.route('/panel/on')
def luzon():
    '''print('luzon')
    flash('Luz prendida','warning')'''
    return render_template('control/panel.html')

@control.route('/panel/off')
def luzoff():
    '''print('luzoff')
    flash('Luz apagada','dark')'''
    return render_template('control/panel.html')

@control.route('/panel/start')
def start():
    '''print('start')
    flash('Inicio')'''
    return render_template('control/panel.html')
    

