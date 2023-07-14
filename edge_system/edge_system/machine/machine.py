from flask import Blueprint, render_template, request, flash
from flask.helpers import url_for
from werkzeug.utils import redirect, secure_filename
from sqlalchemy.sql.expression import and_
import os

from edge_system import db, ALLOWED_EXTENSIONS_FILE, app
from edge_system.machine.model.machine import Machine, RegisterForm
from edge_system.part.model.part import Part

machine = Blueprint('machine', __name__)

def constructor():
   pass

def allowed_extensions_file(filename):
    return '.' in filename and filename.lower().rsplit('.',1)[1] in ALLOWED_EXTENSIONS_FILE

@machine.route('/machine/register', methods=['POST', 'GET'])
def machine_register():
    form = RegisterForm() #meta={'csrf': False}

    if form.validate_on_submit():
        if Machine.query.get(form.id.data):
            flash('Machine already registered!')
            return redirect(url_for('machine.machine_register'))
        machine =  Machine(request.form['id'],
                            request.form['nickname'],
                            request.form['description'],
                            request.form['brand'],
                            request.form['model'],
                            request.form['voltage'],
                            request.form['amperage'],
                            request.form['serie'],
                            request.form['id_line'],
                            request.form['manufacturing_date'],
                            request.form['instalation_date'],
                            request.form['id_supplier'],
                            request.form['run_date'],
                            request.form['file'])

        if form.file.data:
            file = form.file.data
            if allowed_extensions_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                machine.file = filename

        db.session.add(machine)
        db.session.commit()
        flash("Machine information saved locally!!")
        return redirect(url_for('machine.info_all'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('machine/register.html', form = form)

@machine.route('/machine/update/<int:id>', methods=['POST', 'GET'])
def machine_update(id):
    machine = Machine.query.get_or_404(id)

    form = RegisterForm() #meta={'csrf': False}

    if request.method == 'GET':
        form.id.data = machine.id
        form.nickname.data = machine.nickname
        form.description.data = machine.description
        form.brand.data = machine.brand
        form.model.data = machine.model
        form.voltage.data = machine.voltage
        form.amperage.data = machine.amperage
        form.serie.data = machine.serie
        form.id_line.data = machine.id_line
        form.manufacturing_date.data = machine.manufacturing_date
        form.instalation_date.data = machine.instalation_date
        form.id_supplier.data = machine.id_supplier
        form.run_date.data = machine.run_date
        form.file.data = machine.file

    if form.validate_on_submit():
        # actualizar un registro
        machine.nickname = form.nickname.data
        machine.description = form.description.data
        machine.brand = form.brand.data
        machine.model = form.model.data
        machine.voltage = form.voltage.data
        machine.amperage = form.amperage.data
        machine.serie = form.serie.data
        machine.id_line = form.id_line.data
        machine.manufacturing_date = form.manufacturing_date.data
        machine.instalation_date = form.instalation_date.data
        machine.id_supplier = form.id_supplier.data
        machine.run_date = form.run_date.data

        if form.file.data:
         file = form.file.data
         if allowed_extensions_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            machine.file = filename

        db.session.add(machine)
        db.session.commit()
        flash("Maquina actualizada con exito")
        return redirect(url_for('machine.info_all', id=machine.id))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('machine/update.html', machine=machine, form=form)

@machine.route('/machine/<int:id>')
def show(id):
    machine = Machine.query.get_or_404(id)
    return render_template('machine/show.html', machine=machine)


@machine.route('/machine/delete/<int:id>')
def machine_delete(id):
    machine = Machine.query.get_or_404(id)
    part = Part.query.filter(and_(Part.id_machine==id)).all()

    if part:
        flash("Partes fabricadas con esta maquina","danger")
        return redirect(url_for('machine.info_all'))
    
    db.session.delete(machine)
    db.session.commit()
    flash("Maquina borrada con exito")
    return redirect(url_for('machine.info_all'))

@machine.route('/machine/info_all/')
def info_all():
    machines = Machine.query.all()
    print(machines)
    return render_template("machine/machines_info.html", machines = machines)