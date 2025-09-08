# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config  # Import Config class

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load all configurations from Config class

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    

    from .auth.routes import auth_bp
    from .api.routes import api_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(api_bp, url_prefix="/api")

    return app