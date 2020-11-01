from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email


class PatientForm(FlaskForm):

    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    age = StringField('age', validators=[DataRequired()])
    picture = FileField('picture', validators=[
                        FileAllowed(['jpg', 'jpeg', 'png'])])

    email = StringField('email', validators=[
        DataRequired(), Length(min=6, max=100), Email()])

    number = StringField('phone number', validators=[DataRequired()])

    submit = SubmitField('Add')
