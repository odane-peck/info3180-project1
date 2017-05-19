import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = "SUPERCALIFRAGILISTICSECRETKEY"
#app.config['SQLALCHEMY_DATABASE_URI'] = "ubuntu://user:password@localhost/projecto1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://ubuntu:password-01@localhost/CAPSTONE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning
app.debug = True
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/mydatabase.db'
db = SQLAlchemy(app)
CSRF_ENABLED = True
from app import models

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads\\')

ALLOWED_EXTENSIONS = {"png", 'jpg', 'jpeg', 'gif'}


app.config.from_object(__name__)
from app import views
