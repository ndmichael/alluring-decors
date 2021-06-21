from datetime import datetime
from alluringdecors import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    is_staff = db.Column(db.Boolean,)
    is_active = db.Column(db.Boolean,)
    feedbacks = db.relationship('Feedback', backref='feedback', lazy=True)
    requests = db.relationship('Service_request', backref='service_request', lazy=True)

    def __repr__(self):
        return f'{self.username}'

class Category_project(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    projects = db.relationship('Project', backref='project', lazy=True)

    def __repr__(self):
        return f'{self.name}'


class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    client = db.Column(db.String(40), nullable=True)
    description= db.Column(db.String(200), nullable=False)
    image_file = db.Column(db.String, nullable=False, default="default.jpg")
    date_added= db.Column(db.DateTime(200), nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category_project.id'), nullable=False)

    def __repr__(self):
        return f'{self.name}'


class FAQ(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(150), nullable=False)
    answer = db.Column(db.String(400), nullable=False)
    # date_added= db.Column(db.DateTime(200), nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.question}'


class Feedback(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    quality = db.Column(db.String(10), nullable=False)
    suggestion = db.Column(db.String(400), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_sent= db.Column(db.DateTime(200), nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.question}'


class Contact(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    detail = db.Column(db.String(150), nullable=False)
    date_added= db.Column(db.DateTime(200), nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.title}'


class Service_request(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    domain = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    remark = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(), nullable=True, default="recieved")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_sent= db.Column(db.DateTime(200), nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.type}'