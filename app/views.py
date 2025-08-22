from cProfile import Profile
import random
from idlelib.outwin import file_line_progs
from selectors import SelectSelector
from sqlalchemy import select,or_,not_,and_
from cffi.verifier import set_tmpdir
from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory, session,jsonify
from app import app
from app.models import User, UserInfo, MealData, PersonalMealData
from app.forms import ChooseForm, LoginForm, RegistrationForm, UserInfoForm,OwnRecipeForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit
import csv
import io
from fpdf import FPDF
from datetime import datetime
import re
from collections import Counter
import pandas as pd
from flask import request
import numpy as np
import tensorflow as tf
import pickle
import json
from tensorflow.keras.preprocessing.sequence import pad_sequences
import spacy
nlp = spacy.load("en_core_web_sm")



@app.route("/")
def home():
    return render_template('home.html', title="Home")



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user=User(full_name=form.full_name.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Your account has been created!', 'success')
        return redirect(url_for('user_info'))
    return render_template('register.html', title="Register", form=form)

@app.route("/user_info", methods=['GET', 'POST'])
@login_required
def user_info():
    form = UserInfoForm()
    existing_info = db.session.get(UserInfo, current_user.id)

    if form.validate_on_submit():
        allergies = ",".join(form.allergies.data) if form.allergies.data else None
        conditions = form.health_conditions.data or []

        other_condition = form.other_health_condition.data.strip() if form.other_health_condition.data else None
        conditions = [c for c in conditions if c.lower() != "other"]
        if other_condition:
            conditions.append(other_condition)

        health_conditions = ",".join(conditions) if conditions else None

        if existing_info:
            existing_info.age = form.age.data
            existing_info.gender = form.gender.data
            existing_info.height = form.height.data
            existing_info.weight = form.weight.data
            existing_info.diet_type = form.diet_type.data
            existing_info.allergies = allergies
            existing_info.health_conditions = health_conditions
            existing_info.primary_goal = form.primary_goal.data
            existing_info.activity_level = form.activity_level.data
        else:
            user_info = UserInfo(
                user_id=current_user.id,
                age=form.age.data,
                gender=form.gender.data,
                height=form.height.data,
                weight=form.weight.data,
                diet_type=form.diet_type.data,
                allergies=allergies,
                health_conditions=health_conditions,
                primary_goal=form.primary_goal.data,
                activity_level=form.activity_level.data
            )
            db.session.add(user_info)

        db.session.commit()
        flash('Your information has been updated!', 'success')
        return render_template('home.html', title='Home Page')

    return render_template('user_info.html', title='User Info', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html',title='Dashboard', user=current_user)

# @app.route('/mealplan')
# @login_required
# def mealplan():
#     return render_template('mealplan.html',title='Meal Plan')

@app.route('/mealplan_daily')
@login_required
def mealplan_daily():
    user_info = db.session.get(UserInfo, current_user.id)
    if not user_info:
        flash('Please complete your user information first.', 'warning')
        return redirect(url_for('user_info'))

    user_allergies = [a.strip().lower() for a in user_info.allergies.split(',')] if user_info.allergies else []
    user_diet_type = user_info.diet_type.lower() if user_info.diet_type else None
    user_health_conditions = [c.strip().lower() for c in
                              user_info.health_conditions.split(',')] if user_info.health_conditions else []

    mealdata = {}
    session_meal_indices = session.get('meal_indices', {})

    for meal_type in ['Breakfast', 'Lunch', 'Dinner']:
        stmt = select(MealData).where(MealData.meal_type == meal_type)

        if user_diet_type:
            stmt = stmt.where(MealData.diet_type.ilike(f"%{user_diet_type}%"))

        for allergy in user_allergies:
            stmt = stmt.where(not_(MealData.allergens.ilike(f'%{allergy}%')))

        if user_health_conditions:
            health_filters = [MealData.health_conditions.ilike(f'%{cond}%') for cond in user_health_conditions]
            stmt = stmt.where(or_(*health_filters))

        meals = db.session.execute(stmt).scalars().all()

        i = session_meal_indices.get(meal_type, 0)

        if meals:
            i = min(i, len(meals) - 1)
            mealdata[meal_type] = meals[i]
            session_meal_indices[meal_type] = i
        else:
            mealdata[meal_type] = None
            session_meal_indices[meal_type] = 0

    session['meal_indices'] = session_meal_indices
    session.modified = True

    return render_template('meal_plan_daily.html', title='Meal Plan', meals=mealdata)


@app.route('/swap_meal/<meal_type>')
@login_required
def swap_meal(meal_type):
    if meal_type not in ['Breakfast', 'Lunch', 'Dinner']:
        return redirect(url_for('mealplan_daily'))

    user_info = db.session.get(UserInfo, current_user.id)
    if not user_info:
        flash('Please complete your user information first.', 'warning')
        return redirect(url_for('user_info'))

    user_allergies = [a.strip().lower() for a in user_info.allergies.split(',')] if user_info.allergies else []
    user_diet_type = user_info.diet_type
    user_health_conditions = user_info.health_conditions.split(',') if user_info.health_conditions else []

    stmt = select(MealData).where(MealData.meal_type == meal_type)

    if user_diet_type:
        stmt = stmt.where(MealData.diet_type.ilike(f"%{user_diet_type.lower()}%"))

    for allergy in user_allergies:
        stmt = stmt.where(not_(MealData.allergens.ilike(f'%{allergy}%')))

    if user_health_conditions:
        health_filters = [MealData.health_conditions.ilike(f'%{cond.strip()}%') for cond in user_health_conditions]
        stmt = stmt.where(or_(*health_filters))

    meals = db.session.execute(stmt).scalars().all()

    if not meals:
        flash(f'No meals available to swap for {meal_type}.', 'warning')
        return redirect(url_for('mealplan_daily'))

    if 'meal_indices' not in session:
        session['meal_indices'] = {}
    i = session['meal_indices'].get(meal_type, 0)
    i = (i + 1) % len(meals)
    session['meal_indices'][meal_type] = i

    meal = meals[i]

    # Save the selected meal ID in the session for the grocery list later
    session.setdefault('selected_meals', {})
    session['selected_meals'][meal_type] = meal.id  # Store actual meal id

    # Also update meal_indices if you still want to keep track of the index
    if 'meal_indices' not in session:
        session['meal_indices'] = {}
    session['meal_indices'][meal_type] = i

    session.modified = True
    return redirect(url_for('mealplan_daily'))


@app.route('/recipe/<int:meal_id>')
@login_required
def recipe(meal_id):
    meal = db.session.get(MealData, meal_id)
    if not meal:
        flash("Meal not found.", "danger")
        return redirect(url_for('mealplan_daily'))

    return render_template('recipe.html', title='Recipe', meal=meal)


@app.route('/own_recipe', methods=['GET', 'POST'])
@login_required
def own_recipe():
    form = OwnRecipeForm()
    personal_meals = PersonalMealData.query.filter_by(user_id=current_user.id).all()

    # Group meals by meal_type in Python
    meals_by_type = {'Breakfast': [], 'Lunch': [], 'Dinner': []}
    for meal in personal_meals:
        if meal.meal_type in meals_by_type:
            meals_by_type[meal.meal_type].append(meal)
        else:
            meals_by_type[meal.meal_type] = [meal]

    if form.validate_on_submit():
        new_meal = PersonalMealData(
            user_id=current_user.id,
            meal_type=form.meal_type.data,
            meal_name=form.meal_name.data,
            calories=form.calories.data,
            recipe=form.recipe.data
        )
        db.session.add(new_meal)
        db.session.commit()
        flash('Recipe added', 'success')
        return redirect(url_for('own_recipe'))

    return render_template('own_recipe.html', title='Own Recipe', form=form, meals_by_type=meals_by_type)

@app.route('/recipevault', methods=['GET', 'POST'])
@login_required
def recipe_vault():
    df = pd.read_csv('All_Diets.csv') #load data into pandas


    diet_types = sorted(df['Diet_type'].dropna().unique())
    cuisine_types = sorted(df['Cuisine_type'].dropna().unique())

    # Default: show no recipes
    filtered_recipes = []

    if request.method == 'POST':
        selected_diet = request.form.get('diet_type')
        selected_cuisine = request.form.get('cuisine_type')

        # Apply filters
        filtered_recipes = df[
            (df['Diet_type'] == selected_diet) &
            (df['Cuisine_type'] == selected_cuisine)
        ].to_dict(orient='records') #converted to dictionary

    return render_template('recipe_vault.html',
                           title='Recipe Vault',
                           diet_types=diet_types,
                           cuisine_types=cuisine_types,
                           recipes=filtered_recipes)


VERB_PREFIXES = [
    "add", "bake", "blend", "boil", "chop", "combine", "cook", "drizzle", "fill",
    "fry", "garnish", "grill", "heat", "mix", "preheat", "roast", "sauté", "serve",
    "spread", "stir", "toast", "top", "use"
]

UNITS = ['cup', 'cups', 'tbsp', 'tsp', 'slice', 'slices', 'block', 'clove', 'cloves',
         'gram', 'grams', 'ml', 'oz', 'lb', 'kg', 'teaspoon', 'tablespoon']

def extract_ingredients(text):
    lines = text.splitlines() #slplit recipes into lines
    ingredients = set()

    for line in lines:
        line = line.strip().lower()

        # Skip empty lines, headers, or instruction lines starting with "." or digits
        if (not line or
            "instruction" in line or
            "ingredients" in line or
            line.startswith('.') or
            re.match(r'^\d', line)):
            continue

        # Skip lines that start with cooking verbs
        if any(line.startswith(verb) for verb in VERB_PREFIXES):
            continue

        # Remove bullets or dashes
        line = re.sub(r"^[-•]\s*", "", line)

        # Split compound lines on commas or dashes
        parts = re.split(r"[,-]", line)
        for part in parts:
            part = part.strip()

            # Remove quantities and units
            part = re.sub(r'\b(\d+\/\d+|\d+\s?\d*|½|¼|¾)\s*(' + '|'.join(UNITS) + r')?\b', '', part)
            part = part.strip()

            if not part or any(part.startswith(v) for v in VERB_PREFIXES):
                continue

            # Uses spcy to detect nouns
            doc = nlp(part)
            for token in doc:
                if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2:
                    ingredients.add(part)
                    break

    # remove duplicates,irrelevant words
    cleaned = {i.strip() for i in ingredients if i and len(i) > 2 and i != 'ingredients'}
    return sorted(cleaned)

@app.route('/grocery_list')
@login_required
def grocery_list():
    selected_meal_ids = session.get('selected_meals', {}) #get users meal from session
    if not selected_meal_ids:
        flash('No meals selected yet.', 'warning')
        return redirect(url_for('mealplan_daily'))

    meals = db.session.execute(
        select(MealData).where(MealData.id.in_(selected_meal_ids.values()))).scalars().all()

    all_ingredients = []
    for meal in meals:
        recipe_text = meal.recipe
        ingredients = extract_ingredients(recipe_text)
        all_ingredients.extend(ingredients)

    # Remove duplicates and sorts
    grocery_list = sorted(set(all_ingredients))

    # Store grocery list in session for download
    session['grocery_list'] = grocery_list

    return render_template('grocery_list.html', title='Grocery List', ingredients=grocery_list)


def get_current_grocery_list():
    selected_meal_ids = session.get('selected_meals', {}) #retrieve meal from users ession
    if not selected_meal_ids:
        flash('No meals selected yet.', 'warning')
        return None

    meals = db.session.execute(
        select(MealData).where(MealData.id.in_(selected_meal_ids.values()))).scalars().all()

    all_ingredients = []
    for meal in meals:
        all_ingredients.extend(extract_ingredients(meal.recipe)) #add all ingredients to list

    grocery_list = sorted(set(all_ingredients)) #remove dupli
    return grocery_list


@app.route('/update_checkbox', methods=['POST'])
@login_required
def update_checkbox():
    checked_items = request.form.getlist('checked_items')
    session['checked_items'] = checked_items
    flash('Progress saved!', 'success')
    return redirect(url_for('grocery_list'))


@app.route('/download_grocery_pdf')
@login_required
def download_grocery_pdf():
    grocery_list = get_current_grocery_list()
    if grocery_list is None:
        return redirect(url_for('mealplan_daily'))

    checked_items = session.get('checked_items', [])
    remaining_items = [item for item in grocery_list if item not in checked_items]

    if not remaining_items:
        flash('All items are already checked. Nothing to export.', 'warning')
        return redirect(url_for('grocery_list'))

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Grocery List - Remaining Items", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    for item in remaining_items:
        pdf.cell(0, 8, f"- {item}", ln=True) #loop through ingredients in new line

    #not storeed in server
    pdf_bytes = pdf.output(dest='S').encode('latin1')  # get PDF as bytes
    pdf_buffer = io.BytesIO(pdf_bytes)  # put bytes into a buffer

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="grocery_list.pdf",
        mimetype="application/pdf"
    ) #download,filename,pdftype


#trained tensorflow model
model = tf.keras.models.load_model('chatbot_model/chatbot_model.h5')


with open('chatbot_model/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

with open('chatbot_model/label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)

# Load intents
with open('intents.json') as file:
    intents = json.load(file)

#convert user input to lowercase
def preprocess_text(text):
    return text.lower()

@app.route('/chatbot-message', methods=['POST'])
@login_required
def chatbot_message():
    user_input = request.json.get('message')

    sequence = tokenizer.texts_to_sequences([user_input])
    padded_sequence = pad_sequences(sequence, truncating='post', maxlen=20)

    #predict intent
    predictions = model.predict(padded_sequence)[0]
    predicted_index = np.argmax(predictions)
    confidence = predictions[predicted_index]
    predicted_tag = lbl_encoder.inverse_transform([predicted_index])[0]

    print(f"User: {user_input}, Tag: {predicted_tag}, Confidence: {confidence:.2f}")

    print(f"Prediction: {predictions}")
    print(f"Confidence: {confidence:.2f}, Predicted Tag: {predicted_tag}")
    if confidence < 0.0:
        predicted_tag = "no_answer"

    #chooses a response
    for intent in intents["intents"]:
        if intent["tag"] == predicted_tag:
            response = random.choice(intent["responses"])
            return jsonify({'response': response})

    return jsonify({'response': "Sorry, I didn’t understand that."})



@app.route('/profile')
@login_required
def profile():
    user_info=db.session.scalar(sa.select(UserInfo).where(UserInfo.user_id == current_user.id))
    return render_template('profile.html', title='My Profile',user=current_user,user_info=user_info)

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user_info = db.session.get(UserInfo, current_user.id)
    if user_info:
        db.session.delete(user_info)
    user = db.session.get(User, current_user.id)
    if user:
        db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted.', 'info')
    logout_user()
    return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Error'), 403

# Handler for 404 Not Found
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Error'), 404

@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html', title='Error'), 413

# 500 Internal Server Error
@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500


