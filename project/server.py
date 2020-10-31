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
from forms.login_form import LoginForm
from forms.account_form import AccountForm


#app, bcrypt, db, login_manager = init.create_app()

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


@app.route("/about", methods=['GET'])
def about():
    return rt('about.html', title='About')


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    if form.validate_on_submit():
        print(f'firstname:{current_user.user_firstname} lastname: {current_user.user_lastname} email: {current_user.user_lastname} age: {current_user.user_age}', flush=True)
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
    return rt('account.html', title='Account', image=img, form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data.strip()).first()
        if user and bcrypt.check_password_hash(user.user_password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome to your workspace {form.email.data}!', 'success')
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


@app.route("/userid/<int:userid>", methods=['GET'])
@login_required
def fetch_userid(userid):
    user = User.query.filter_by(id=userid).first()
    # user = User.query.filter(User.id=userid).first()
    return jsonify(success=True, user=user.serialize)


@app.route("/useremail/<string:email>", methods=['GET'])
@login_required
def fetch_useremail(email):
    user = User.query.filter_by(user_email=email).first()
    return jsonify(success=True, user=user.serialize)


@app.route("/add", methods=['GET'])
def add_user():
    fname = request.args.get('fname')
    lname = request.args.get('lname')
    age = request.args.get('age')
    category = request.args.get('category')

    user = User(user_firstname=fname, user_lastname=lname,
                user_age=age, user_category=Category(category_name=category))
    db.session.add(user)
    db.session.commit()
    return jsonify(success=True)


@app.route("/addnote", methods=['GET'])
@login_required
def add_note():
    note = request.args.get('note')

    note = Note(note_content=content)
    db.session.add(note)
    db.session.commit()
    return jsonify(success=True)


@app.route("/sessions", methods=['GET'])
@login_required
def render_all_sessions():
    all_sessions = Session.query.all()

    return rt('sessions.html', sessions=all_sessions)


@app.route("/addpatient", methods=['GET'])
@login_required
def add_patient():
    email = request.args.get('email')
    fname = request.args.get('fname')
    lname = request.args.get('lname')
    age = request.args.get('age')
    phone = request.args.get('phone')

    patient = Patient(patient_firstname=fname, patient_lastname=lname,
                      patient_age=age, patient_email=email, patient_phone_number=phone)
    db.session.add(patient)
    db.session.commit()
    return jsonify(success=True)


@app.route("/patients", methods=['GET'])
@login_required
def fetch_all_patients():
    all_patients = Patient.query.all()
    res = []
    for patient in all_patients:
        res.append(patient.serialize)

    return jsonify(success=True, patients=res)


@app.route("/patient/<int:patientid>", methods=['GET'])
@login_required
def patient(patientid):
    patient = Patient.query.filter_by(patient_id=patientid).first()

    return jsonify(success=True, patient=patient.serialize)


@app.route("/mock", methods=['GET'])
def mock():

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
    for i in range(5):
        patient = Patient(patient_firstname=f'john{rd.randint(1,1000)}', patient_lastname=f'doe{rd.randint(1,1000)}',
                          patient_age=rd.randint(10, 100), patient_email=f'john{rd.randint(1,1000)}@doe.co',
                          patient_phone_number=f'+336776655{rd.randint(10,99)}', user_id=all_users[0]['id'])
        try:
            db.session.add(patient)
            db.session.commit()
            all_patients.append(patient.serialize)
        except:
            print('patient error: ', str(e))
            db.session.rollback()
    all_sessions = []
    for i in range(10):
        ses = Session(session_notes=f'jot down something: {rd.randint(1,1000)}', session_user_id=all_users[
                      0]['id'], session_patient_id=all_patients[rd.randint(0, len(all_patients) - 1)]['id'])
        try:
            db.session.add(ses)
            db.session.commit()
            all_sessions.append(ses.serialize)
        except Exception as e:
            print('session error: ', str(e))
            db.session.rollback()
            raise e

    return jsonify(success=True, users=all_users, patients=all_patients, sessions=all_sessions)
