from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

#Check for SQL querries keywords to prevent SQL Injection attacks
def validate_SQL(input_string):
    for i in range(len(input_string)):
        if input_string[i:i+6] == "SELECT":
            flash("Please refrain from entering SQL querries!", category='error')
            return False
        elif input_string[i:i+5] == "WHERE" or input_string[i:i+5] == "UNION":
            flash("Please refrain from entering SQL querries!", category='error')
            return False
        elif input_string[i:i+4] == "DROP" or input_string[i:i+4] == "FROM":
            flash("Please refrain from entering SQL querries!", category='error')
            return False
        elif input_string[i:i+3] == "AND":
            flash("Please refrain from entering SQL querries!", category='error')
            return False
    return True

#Check for XSS cross site scripting by preventing entry of javascript code
def validate_JS(input_string):
    for i in range(len(input_string)):
        if input_string[i:i+9] == "<script>":
            flash("Please refrain from entering javascript code!", category='error')
            return False
    return True

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = '{}'.format(email)).first()

        #No SQL injection attack or XSS attack entries 
        if validate_JS(email) and validate_JS(password) and validate_SQL(email) and validate_SQL(password):
            if check_password_hash(user.password, password):
                flash('Logged in successfully! Welcome back '+user.first_name+" "+user.last_name+".", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password", category='error')
        else:
            flash('Email does not exist, please create an account', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = '{}'.format(email)).first()

        if user:
            flash("Email is already registered, please login to account.", category='error')
        elif len(email) < 4:
            flash("Incorrect email, please enter again.", category='error')
        elif password1 != password2:
            flash("Passwords do not match, please enter again.", category='error')
        elif len(password1) < 5:
            flash("Password must be at least 5 characters long, please enter again.", category='error')
        else:
            new_user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Your new account has been created.", category='success')
            
            return redirect(url_for('views.home'))
    
    return render_template("sign_up.html", user=current_user)

@auth.route('/about_us', methods=['GET','POST'])
def about():
    return render_template("about.html", user=current_user)
