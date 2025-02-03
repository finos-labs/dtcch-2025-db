# app/__init__.py
from flask import Flask
from .routes import main_routes
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # Load configuration from config.py
    app.config.from_pyfile('../config.py')
    db.init_app(app)

    # Register blueprints or routes
    app.register_blueprint(main_routes)

    return app