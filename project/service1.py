from flask import request, jsonify, render_template as rt
import os
import time
import datetime
import json
import random as rd

import init
from models import User, db, Patient, Session


app = init.create_app()
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
    return rt('about.html')


@app.route("/users", methods=['GET'])
def fetch_all_users():
    all_users = User.query.all()
    res = []
    for user in all_users:
        # res.append({'id': user.user_id,
        #             'firstname': user.user_firstname,
        #             'lastname': user.user_lastname,
        #             'age': user.user_age})

        res.append(user.serialize)
    return jsonify(success=True, users=res)


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


@app.route("/addcategory", methods=['GET'])
def add_category():
    name = request.args.get('name')

    category = Category(category_name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify(success=True)


@app.route("/categories", methods=['GET'])
def fetch_all_categories():
    all_catg = Category.query.all()
    res = []
    for catg in all_catg:
        res.append(catg.serialize)

    return jsonify(success=True, categories=res)


@app.route("/addnote", methods=['GET'])
def add_note():
    note = request.args.get('note')

    note = Note(note_content=content)
    db.session.add(note)
    db.session.commit()
    return jsonify(success=True)


@app.route("/sessions", methods=['GET'])
def fetch_all_sessions():
    all_sessions = Session.query.all()

    return jsonify(success=True, sessions=[ses.serialize for ses in all_sessions])


@app.route("/addpatient", methods=['GET'])
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
def fetch_all_patients():
    all_patients = Patient.query.all()
    res = []
    for patient in all_patients:
        res.append(patient.serialize)

    return jsonify(success=True, patients=res)


@app.route("/mock", methods=['GET'])
def mock():
    all_users = []
    for i in range(2):
        user = User(user_firstname=f'user{rd.randint(1,1000)}', user_lastname=f'lastname{rd.randint(1,1000)}',
                    user_age=rd.randint(20, 65))
        try:
            db.session.add(user)
            db.session.commit()
            all_users.append(user.serialize)
        except:
            print('user error: ', str(e))
            db.session.rollback()

    all_patients = []
    for i in range(5):
        patient = Patient(patient_firstname=f'john{rd.randint(1,1000)}', patient_lastname=f'doe{rd.randint(1,1000)}',
                          patient_age=rd.randint(10, 100), patient_email=f'john{rd.randint(1,1000)}@doe.co',
                          patient_phone_number=f'+336776655{rd.randint(10,99)}', user_id=all_users[rd.randint(
                              0, len(all_users) - 1)]['id'])
        try:
            db.session.add(patient)
            db.session.commit()
            all_patients.append(patient.serialize)
        except:
            print('patient error: ', str(e))
            db.session.rollback()
    all_sessions = []
    for i in range(10):
        ses = Session(session_notes=f'jot down something: {rd.randint(1,1000)}', session_user_id=all_users[rd.randint(
            0, len(all_users) - 1)]['id'], session_patient_id=all_patients[rd.randint(0, len(all_patients) - 1)]['id'])
        try:
            db.session.add(ses)
            db.session.commit()
            all_sessions.append(ses.serialize)
        except Exception as e:
            print('session error: ', str(e))
            db.session.rollback()
            raise e

    return jsonify(success=True, users=all_users, patients=all_patients, sessions=all_sessions)
