from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from models import User


class LoginForm(FlaskForm):
    email = StringField('email', validators=[
                        DataRequired(), Length(min=6, max=100), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember me')

    submit = SubmitField('sign in')
