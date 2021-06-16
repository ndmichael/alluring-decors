from datetime import datetime
from alluringdecors import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    is_staff = db.Column(db.Boolean,)
    is_active = db.Column(db.Boolean,)

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