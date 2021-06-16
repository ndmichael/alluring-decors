from flask import Flask, render_template, url_for, flash, redirect
from alluringdecors.forms import RegistrationForm, LoginForm
from alluringdecors.models import User, Category_project, Project
from alluringdecors import app

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
        flash(f'Account successfully create for {form.username.data}', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title='register', form=form)

@app.route("/login/", methods=['GET', 'POST'])
def login():   
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == '1234':
            flash(f'Login successful for {form.email.data}', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'Login unsuccessful check username or password', 'danger')

    return render_template("login.html", title='Login', form=form)