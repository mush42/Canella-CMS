from flask import Flask, request, g, abort
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
from flask_migrate import Migrate
from flask_wtf import CsrfProtect
from functools import wraps
from sqlalchemy_continuum.plugins import FlaskPlugin
from sqlalchemy_continuum import make_versioned
from .util.page import PathToSlugConvertor

app = Flask("canella")

# Configuration
app.config.from_pyfile('config.py')
app.url_map.converters['slug'] = PathToSlugConvertor

# Extentions
db = SQLAlchemy(app)
make_versioned(plugins=[FlaskPlugin()])
babel = Babel(app)
migrate = Migrate(app=app, db=db)
csrf = CsrfProtect(app)

from .main import *
