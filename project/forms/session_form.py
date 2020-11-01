from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from models import User


class SessionForm(FlaskForm):
    notes = TextAreaField('notes', validators=[DataRequired(), Length(min=1)])

    submit = SubmitField('Add Session')
