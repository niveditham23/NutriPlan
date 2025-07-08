from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, PasswordField, BooleanField, SelectField,IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError, Email, Optional, Length
from app import db
from app.models import User
import datetime


class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')



def password_policy(form, field):
    message = """A password must be at least 8 characters long and contain an
                 uppercase letter, a lowercase letter, a digit, and a special character."""
    if len(field.data) < 8:
        raise ValidationError(message)
    flg_upper = flg_lower = flg_digit = flg_special = False
    for ch in field.data:
        if ch.isupper():
            flg_upper = True
        elif ch.islower():
            flg_lower = True
        elif ch.isdigit():
            flg_digit = True
        elif not ch.isalnum():
            flg_special = True
    if not (flg_upper and flg_lower and flg_digit and flg_special):
        raise ValidationError(message)

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), password_policy])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Your Account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please log in or use a different email.')
