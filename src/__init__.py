# Import flask and template operators
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

basic_auth = HTTPBasicAuth()
app = Flask(__name__)
db = SQLAlchemy()



