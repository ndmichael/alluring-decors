from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

  
app = Flask(__name__)
app.config['SECRET_KEY'] = '2523b14a259b1e38d321f17132f5fcf8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

from alluringdecors import routes