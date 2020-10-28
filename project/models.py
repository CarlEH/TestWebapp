import flask_sqlalchemy
from sqlalchemy.sql import func

db = flask_sqlalchemy.SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_firstname = db.Column(db.String(128))
    user_lastname = db.Column(db.String(128))
    user_age = db.Column(db.Integer)
    user_email = db.Column(db.String(256))
    user_phone_numbber = db.Column(db.String(32))
    patients = db.relationship(
        'Patient', backref=db.backref('patient', lazy='joined'))

    # def __init__(self, **kwargs):
    #     #self.user_id = kwargs.get('user_id')
    #     self.user_firstname = kwargs.get('user_firstname')
    #     self.user_lastname = kwargs.get('user_lastname')
    #     self.user_age = kwargs.get('user_age')
    #     self.categories = kwargs.get('user_category')

    @property
    def serialize(self):
        return {'id': self.user_id,
                'firstname': self.user_firstname,
                'lastname': self.user_lastname,
                'age': self.user_age,
                'patients': [patient.serialize for patient in self.patients]}


class Patient(db.Model):
    __tablename__ = 'patient'
    patient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    patient_firstname = db.Column(db.String(128))
    patient_lastname = db.Column(db.String(128))
    patient_age = db.Column(db.Integer)
    patient_email = db.Column(db.String(256))
    patient_phone_number = db.Column(db.String(32))
    patient_creation_date = db.Column(db.DateTime(
        timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id'), nullable=True)

    # def __init__(self, **kwargs):
    #     self.patient_id = kwargs.get('user_id')
    #     self.patient_firstname = kwargs.get('patient_firstname')
    #     self.patient_lastname = kwargs.get('patient_lastname')
    #     self.patient_email = kwargs.get('patient_email')
    #     self.patient_age = kwargs.get('patient_age')
    #     self.patient_phone_number = kwargs.get('patient_phone_number')
    #     self.user_id = kwargs.get('user_id')

    @property
    def serialize(self):
        return {'id': self.patient_id,
                'firstname': self.patient_firstname,
                'lastname': self.patient_lastname,
                'email': self.patient_email,
                'age': self.patient_age,
                'email': self.patient_email,
                'phone_number': self.patient_phone_number,
                'user_id:': self.user_id}


class Session(db.Model):
    __tablename__ = 'session'
    session_id = db.Column(db.Integer, primary_key=True)
    session_notes = db.Column(db.Text())
    session_user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id'), nullable=True)
    session_patient_id = db.Column(db.Integer, db.ForeignKey(
        'patient.patient_id'), nullable=True)
    session_creation_date = db.Column(db.DateTime(
        timezone=True), server_default=func.now())

    # def __init__(self, **kwargs):
    #     #self.note_id = kwargs.get('note_id')
    #     self.note_content = kwargs.get('note_content')
    #     self.note_creation_date = kwargs.get('note_creation_date')

    @property
    def serialize(self):
        return {'id': self.session_id,
                'notes': self.session_notes,
                'user_id': self.session_user_id,
                'patient_id': self.session_patient_id,
                'creation date': self.session_creation_date}