from flask import Flask
from flask_sqlalchemy import SQLAlchemy

"""Construct the core application."""
app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')

db.init_app(app)

db = SQLAlchemy(app)
