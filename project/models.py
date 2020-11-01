import flask_sqlalchemy
from sqlalchemy.sql import func

from flask_login import UserMixin

db = flask_sqlalchemy.SQLAlchemy()
from init import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,  UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_firstname = db.Column(db.String(128))
    user_lastname = db.Column(db.String(128))
    user_age = db.Column(db.Integer)
    user_email = db.Column(db.String(256), unique=True, nullable=False)
    user_password = db.Column(db.String(128), nullable=False)
    user_phone_numbber = db.Column(db.String(32))
    user_img = db.Column(db.String(40), default='default_profile.jpeg')
    patients = db.relationship(
        'Patient', backref=db.backref('nutritionist', lazy=True))

    @property
    def serialize(self):
        return {'id': self.id,
                'firstname': self.user_firstname,
                'lastname': self.user_lastname,
                'age': self.user_age,
                'email': self.user_email,
                'phone': self.user_phone_numbber,
                'patients': [patient.serialize for patient in self.patients]}


class Patient(db.Model):
    __tablename__ = 'patient'
    patient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    patient_firstname = db.Column(db.String(128))
    patient_lastname = db.Column(db.String(128))
    patient_age = db.Column(db.Integer)
    patient_email = db.Column(db.String(256))
    patient_phone_number = db.Column(db.String(32))
    patient_img = db.Column(db.String(40), default='default_profile.jpeg')
    patient_creation_date = db.Column(db.DateTime(
        timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=True)
    sessions = db.relationship(
        'Session', backref=db.backref('patient', lazy=True))

    @property
    def serialize(self):
        return {'id': self.patient_id,
                'firstname': self.patient_firstname,
                'lastname': self.patient_lastname,
                'email': self.patient_email,
                'age': self.patient_age,
                'email': self.patient_email,
                'phone_number': self.patient_phone_number,
                'user_id:': self.user_id,
                'sessions': [session.serialize for session in self.sessions]}


class Session(db.Model):
    __tablename__ = 'session'
    session_id = db.Column(db.Integer, primary_key=True)
    session_notes = db.Column(db.Text())
    session_user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    session_patient_id = db.Column(db.Integer, db.ForeignKey(
        'patient.patient_id'), nullable=False)
    session_creation_date = db.Column(db.DateTime(
        timezone=True), server_default=func.now())

    @property
    def serialize(self):
        return {'id': self.session_id,
                'notes': self.session_notes,
                'user_id': self.session_user_id,
                'patient_id': self.session_patient_id,
                'creation date': self.session_creation_date}
