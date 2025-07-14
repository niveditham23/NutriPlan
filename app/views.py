from cProfile import Profile

from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory
from app import app
from app.models import User,UserInfo
from app.forms import ChooseForm, LoginForm, RegistrationForm, UserInfoForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit
import csv
import io
import datetime


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
def user_info():
    form = UserInfoForm()
    existing_info = db.session.get(UserInfo, current_user.id)
    if form.validate_on_submit():
        allergies = ",".join(form.allergies.data) if form.allergies.data else None
        health_conditions = ",".join(form.health_conditions.data) if form.health_conditions.data else None

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
            user_info=UserInfo(user_id=current_user.id,age=form.age.data,gender=form.gender.data,height=form.height.data,weight=form.weight.data,diet_type=form.diet_type.data,allergies=allergies,health_conditions=health_conditions,primary_goal=form.primary_goal.data,activity_level=form.activity_level.data)
            db.session.add(user_info)
        db.session.commit()
        flash('Your information has been updated!', 'success')
        return render_template('dashboard.html', title='Dashboard')
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

@app.route('/mealplan')
@login_required
def meal_plan():
    return render_template('meal_plan.html', title='Meal Plan')

@app.route('/recipevault')
@login_required
def recipe_vault():
    return render_template('recipe_vault.html', title='Recipe Vault')


@app.route('/grocerylist')
@login_required
def grocery_list():
    return render_template('grocery_list.html', title='Grocery List')

@app.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html', title='Notifications')


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


# Error handlers
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

# Error handler for 403 Forbidden
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



# <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
#   <div class="container-fluid">
#     <a class="navbar-brand" href="{{ url_for('home') }}">NutriPlan</a>
#
#     <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
#       aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
#       <span class="navbar-toggler-icon"></span>
#     </button>
#
#     <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
#       <ul class="navbar-nav flex-grow-1 d-flex justify-content-start gap-3">
#         <li class="nav-item"><a class="nav-link" href="{{ url_for('home') }}">Home</a></li>
#         {% if current_user.is_authenticated %}
#           <li class="nav-item"><a class="nav-link" href="{{ url_for('meal_plan') }}">Meal Plan</a></li>
#           <li class="nav-item"><a class="nav-link" href="{{ url_for('recipe_vault') }}">Recipe Vault</a></li>
#           <li class="nav-item"><a class="nav-link" href="{{ url_for('grocery_list') }}">Grocery List</a></li>
#         {% endif %}
#       </ul>
#
#       <ul class="navbar-nav d-flex align-items-center gap-3">
#         {% if current_user.is_authenticated %}
#           <li class="nav-item">
#             <a class="nav-link" href="{{ url_for('notifications') }}">
#               <i class="bi bi-bell fs-4"></i>
#             </a>
#           </li>
#           <li class="nav-item dropdown">
#             <a class="nav-link dropdown-toggle" href="#" id="navbarProfileDropdown" role="button"
#               data-bs-toggle="dropdown" aria-expanded="false">
#               <i class="bi bi-person-circle fs-4"></i>
#             </a>
#             <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarProfileDropdown">
#               <li><a class="dropdown-item" href="{{ url_for('profile') }}">My Profile</a></li>
#               <li><hr class="dropdown-divider"></li>
#               <li><a class="dropdown-item text-danger" href="{{ url_for('logout') }}">Logout</a></li>
#             </ul>
#           </li>
#         {% else %}
#           <li class="nav-item"><a class="nav-link" href="{{ url_for('login') }}">Login</a></li>
#           <li class="nav-item"><a class="nav-link" href="{{ url_for('register') }}">Register</a></li>
#         {% endif %}
#       </ul>
#     </div>
#   </div>
# </nav>
#
# Profile.html
# {% extends "base.html" %}
#
# {% block content %}
# <h4 class="mb-3">Profile and Preferences</h4>
# <div class="row mb-5">
#     <div class="col-lg-6">
#         <div class="table-responsive">
#             <table class="table table-bordered">
#                 <thead class="table-success">
#                     <tr><th>Full Name</th><td>{{ user.full_name }}</td></tr>
#                     <tr><th>Email</th><td>{{ user.email }}</td></tr>
#                 </thead>
#             </table>
#
#             {% if user_info %}
#             <table class="table table-bordered">
#                 <thead class="table-success">
#                     <tr><th>Age</th><td>{{ user_info.age }}</td></tr>
#                     <tr><th>Gender</th><td>{{ user_info.gender }}</td></tr>
#                     <tr><th>Height (cm)</th><td>{{ user_info.height }}</td></tr>
#                     <tr><th>Weight (kg)</th><td>{{ user_info.weight }}</td></tr>
#                     <tr><th>Diet Type</th><td>{{ user_info.diet_type }}</td></tr>
#                     <tr><th>Allergies</th><td>{{ user_info.allergies or 'None' }}</td></tr>
#                     <tr><th>Health Conditions</th><td>{{ user_info.health_conditions or 'None' }}</td></tr>
#                     <tr><th>Primary Goal</th><td>{{ user_info.primary_goal }}</td></tr>
#                     <tr><th>Activity Level</th><td>{{ user_info.activity_level }}</td></tr>
#                 </thead>
#             </table>
#             {% else %}
#             <p class="text-muted">No health info added yet.</p>
#             {% endif %}
#         </div>
#     </div>
# </div>
# {% endblock %}
