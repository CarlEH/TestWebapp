from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from models import User


class AccountForm(FlaskForm):

    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    age = StringField('age', validators=[DataRequired()])

    email = StringField('email', validators=[
        DataRequired(), Length(min=6, max=100), Email()])

    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.user_email:
            user = User.query.filter_by(
                user_email=email.data.strip()).first()
            if user:
                raise ValidationError('email address already in use')
