from flask import Flask, render_template, url_for, flash, redirect
from alluringdecors.forms import RegistrationForm, LoginForm
from alluringdecors.models import User, Category_project, Project
from alluringdecors import app, db, bcrypt
from flask_login import login_user

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, is_active=True, is_staff=False)
        db.session.add(user)
        db.session.commit()
        flash(f'Account successfully create for {form.username.data} you can now login', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title='register', form=form)

@app.route("/login/", methods=['GET', 'POST'])
def login():   
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'You are login as {user.username}', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'login unsuccessful check email or password', 'success')
    return render_template("login.html", title='Login', form=form)