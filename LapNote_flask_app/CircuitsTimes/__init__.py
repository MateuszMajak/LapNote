#!/usr/bin/env python
# coding: utf-8
# In[ ]:

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '88E191B55D751F2768BDCF9F5F825'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web.db?check_same_thread=False'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from CircuitsTimes import views

# In[ ]:
