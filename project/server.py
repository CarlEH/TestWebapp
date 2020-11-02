from flask import request, jsonify, render_template as rt, url_for, flash, redirect
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required, current_user
import os
import time
import datetime
import json
import random as rd

from init import flask_app as app, bcrypt, login_manager, db

from models import User, Patient, Session
from utils import save_picture
from forms.login_form import LoginForm
from forms.account_form import AccountForm
from forms.session_form import SessionForm
from forms.patient_form import PatientForm


os.environ['TZ'] = 'Europe/Paris'
time.tzset()


@app.errorhandler(400)
def error_400(e):
    return jsonify(success=False, error=str(e)), 400


@app.route("/health", methods=['GET'])
def health():
    date = datetime.datetime.fromtimestamp(
        time.time()).strftime('%Y-%m-%d %H:%M')
    return jsonify(success=True, process=os.getpid(), date=date)


@app.route("/check", methods=['GET'])
def check():
    return jsonify(success=True)


@app.route("/faq", methods=['GET'])
def faq():
    return rt('faq.html', title='About')


@app.route("/", methods=['GET'])
def index():
    return redirect(url_for('account'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, app)
            current_user.user_img = picture_file

        current_user.user_firstname = form.firstname.data
        current_user.user_lastname = form.lastname.data
        current_user.user_age = form.age.data
        current_user.user_email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.firstname.data = current_user.user_firstname
        form.lastname.data = current_user.user_lastname
        form.age.data = current_user.user_age
        form.email.data = current_user.user_email

    img = url_for('static', filename=f'profile_pics/{current_user.user_img}')
    current_user.patients.sort(key=lambda p:  p.patient_lastname)

    return rt('account.html', title='Account', image=img, form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data.strip()).first()
        if user and bcrypt.check_password_hash(user.user_password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(
                f'Welcome to your workspace {user.user_firstname}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('account'))

        else:
            flash('Please check you email/password and try again', 'danger')
    return rt('login.html', title='Login', form=form)


@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/users", methods=['GET'])
@login_required
def fetch_all_users():
    all_users = User.query.all()
    res = []
    for user in all_users:
        res.append(user.serialize)
    return jsonify(success=True, users=res)


@app.route("/new/patient", methods=['GET', 'POST'])
@login_required
def add_patient():
    form = PatientForm()
    patient = None
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, app)
            patient = Patient(patient_firstname=form.firstname.data, patient_lastname=form.lastname.data, user_id=current_user.id,
                              patient_age=form.age.data, patient_email=form.email.data, patient_phone_number=form.number.data, patient_img=picture_file)
        else:
            patient = Patient(patient_firstname=form.firstname.data, patient_lastname=form.lastname.data, user_id=current_user.id,
                              patient_age=form.age.data, patient_email=form.email.data, patient_phone_number=form.number.data)
        db.session.add(patient)
        db.session.commit()
        flash('New Patient Added!', 'success')
        return redirect(url_for('patient', patientid=patient.patient_id))

    return rt('new_patient.html', title="New Patient", form=form)


@app.route("/patient/<int:patientid>", methods=['GET', 'POST'])
@login_required
def patient(patientid):
    patient = Patient.query.filter_by(patient_id=patientid).first()
    patient.sessions.sort(key=lambda s: s.session_creation_date)

    form = SessionForm()
    if form.validate_on_submit():
        new_sesssion = Session(session_notes=form.notes.data,
                               session_user_id=current_user.id, session_patient_id=patientid)
        db.session.add(new_sesssion)
        db.session.commit()
        flash('New Session Added!', "success")
        return redirect(url_for('patient', patientid=patientid))

    return rt('patient.html', patient=patient, form=form)


@app.route("/mock", methods=['GET'])
def mock():
    firstnames = ['Emily', 'Djamila', 'Sophie', 'John',
                  'Alan', 'David', 'Daniel', 'Richard', 'Kevin', 'Stephy', 'Camille', 'Guillaume', 'Dani']
    lastnames = ['Doe', 'Smith', 'Chirac', 'Van Hertzen',
                 'Ali', 'Girard', 'Campion', 'Holler', 'Dimitrios', 'Schwartz', 'Lee', 'Vamaux']

    all_users = []

    hsd_pswd = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(user_firstname='admin', user_lastname='root', user_password=hsd_pswd,
                user_age=33, user_email='admin@cuure.co')
    try:
        db.session.add(user)
        db.session.commit()
        all_users.append(user.serialize)
    except Exception as e:
        print('user error: ', str(e))
        db.session.rollback()

    for i in range(2):
        hsd_pswd = bcrypt.generate_password_hash(
            f'password{rd.randint(1,1000)}').decode('utf-8')
        user = User(user_firstname='dr.', user_lastname=f'smith{rd.randint(1,1000)}', user_password=hsd_pswd,
                    user_age=rd.randint(25, 65), user_email=f'doc{rd.randint(1,100)}@cuure.co')
        try:
            db.session.add(user)
            db.session.commit()
            all_users.append(user.serialize)
        except Exception as e:
            print('user error: ', str(e))
            db.session.rollback()

    all_patients = []
    for i in range(10):
        patient = Patient(patient_firstname=firstnames[rd.randint(0, len(firstnames) - 1)],
                          patient_lastname=lastnames[
                              rd.randint(0, len(lastnames) - 1)],
                          patient_age=rd.randint(10, 100), patient_email=f'email{rd.randint(1,1000)}@mail.com',
                          patient_phone_number=f'+336776655{rd.randint(10,99)}', user_id=all_users[0]['id'])
        try:
            db.session.add(patient)
            db.session.commit()
            all_patients.append(patient.serialize)
        except:
            print('patient error: ', str(e))
            db.session.rollback()
    all_sessions = []
    for i in range(20):
        ses = Session(session_notes=f'jot down something: lorem ipsum \n {rd.randint(1,1000)} \n looks promising', session_user_id=all_users[
                      0]['id'], session_patient_id=all_patients[rd.randint(0, len(all_patients) - 1)]['id'],
                      session_creation_date=datetime.datetime(year=2020, month=rd.randint(1, 12), day=rd.randint(1, 28)))
        try:
            db.session.add(ses)
            db.session.commit()
            all_sessions.append(ses.serialize)
        except Exception as e:
            print('session error: ', str(e))
            db.session.rollback()
            raise e
    return redirect('login')
