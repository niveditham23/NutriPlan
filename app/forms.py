from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, PasswordField, BooleanField, SelectField,IntegerField,SelectMultipleField,widgets,FloatField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError, Email, Optional, Length
from app import db
from app.models import User
import datetime


class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
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


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class UserInfoForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=1, max=120)])
    gender = SelectField('Gender',choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],validators=[DataRequired()])
    height = FloatField('Height (in cm)', validators=[DataRequired(), NumberRange(min=100, max=300)])
    weight = FloatField('Weight (in kg)', validators=[DataRequired(), NumberRange(min=30, max=200)])
    diet_type = SelectField('Diet Type',choices=[('Veg', 'Vegetarian'),('Non-Veg', 'Non-Vegetarian'),('Vegan', 'Vegan'),('Keto', 'Keto'),('Paleo', 'Paleo'),('Mediterranean','Mediterranean'),('Other', 'Other')],validators=[DataRequired()])
    allergies = MultiCheckboxField('Allergies',choices=[('Gluten', 'Gluten'),('Treenut', 'Treenut'),('soya', 'Soya'),('milk', 'Milk'),('eggs', 'Eggs'),('fish', 'Fish'),('shellfish', 'Shellfish'),('wheat', 'Wheat'),('peanuts', 'Peanuts'),('sesame', 'Sesame'),('mustard', 'Mustard'),('celery', 'Celery'),('sulfites', 'Sulfites'),],validators=[Optional()])
    primary_goal = SelectField('Primary Goal',choices=[('Lose', 'Lose Weight'),('Maintain', 'Maintain Weight'),('Gain', 'Gain Weight')],validators=[DataRequired()])
    health_conditions = MultiCheckboxField('Health Conditions',choices=[('Diabetes', 'Diabetes'),('PCOS', 'PCOS'),('Thyroid', 'Thyroid'),('Other','Other')],validators=[Optional()])
    other_health_condition=StringField('If Other, specify here', validators=[Optional()])
    activity_level = SelectField('Activity Level',choices=[('Sedentary', 'Sedentary'),('Lightly Active', 'Lightly Active'),('Moderately Active', 'Moderately Active'),('Very Active', 'Very Active')],validators=[DataRequired()])
    submit = SubmitField("Submit")

class OwnRecipeForm(FlaskForm):
    meal_type = SelectField('Meal Type',choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner')],validators=[DataRequired()])
    meal_name = StringField('Meal Name', validators=[DataRequired()])
    calories = IntegerField('Calories', validators=[DataRequired()])
    recipe = TextAreaField('Recipe(Ingredients and Instructions)', validators=[DataRequired()])
    submit = SubmitField("Add Meal")