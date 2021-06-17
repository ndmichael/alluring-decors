from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from alluringdecors.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import (DataRequired, Length, Email , EqualTo, ValidationError)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Now')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username taken please try another')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email eixted already!!!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ProjectCategoryForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    submit = SubmitField('Create')

class NewProjectForm(FlaskForm):
    choices = (
        ('ongoing project', 'Ongoing Project'),
        ('upcoming project', 'Upcoming Project'),
        ('accomplished project', 'Accomplished Project'),
    )
    category = SelectField('Category', choices=[])
    name = StringField('Project Name', validators=[DataRequired()])
    picture = FileField('Project Image', validators=[FileAllowed(['jpg', 'png'])])
    client = StringField('Client', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Project')


class FAQForm(FlaskForm):
    question = StringField('Project Name', validators=[DataRequired()])
    answer = TextAreaField('Project Name', validators=[DataRequired()])
    submit = SubmitField('Submit')