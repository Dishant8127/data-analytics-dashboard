# # backend/app/__init__.py

import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_cors import CORS
from flask_caching import Cache
from flask_migrate import Migrate
from clickhouse_connect import get_client as get_ch_client

# Load environment variables from .env
load_dotenv()

# Global extension instances
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
mail = Mail()
cache = Cache()
migrate = Migrate()
clickhouse_client = None


def create_app():
    app = Flask(__name__)

    # Config
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "fallback-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "fallback-jwt")

    # Mail
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "true").lower() in ["true", "1", "yes"]
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    # Redis / Cache
    app.config["CACHE_TYPE"] = "RedisCache"
    app.config["CACHE_REDIS_URL"] = os.getenv("REDIS_URL", "redis://redis:6379/0")

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    #  CORS fix → allow frontend + expose headers for file download
    CORS(
        app,
        resources={r"/api/*": {"origins": ["http://localhost:5173"]}, r"/auth/*": {"origins": ["http://localhost:5173"]}},
        supports_credentials=True,
        expose_headers=["Content-Disposition"]
    )

    # ClickHouse client
    global clickhouse_client
    try:
        clickhouse_client = get_ch_client(
            host=os.getenv("CLICKHOUSE_HOST", "clickhouse"),
            port=int(os.getenv("CLICKHOUSE_PORT", 9000)),
            username=os.getenv("CLICKHOUSE_USER", "default"),
            password=os.getenv("CLICKHOUSE_PASSWORD", ""),
            database=os.getenv("CLICKHOUSE_DATABASE", "default"),
        )
    except Exception:
        clickhouse_client = None

    # Blueprints
    from app.api.routes import api_bp
    from app.auth.routes import auth_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app

