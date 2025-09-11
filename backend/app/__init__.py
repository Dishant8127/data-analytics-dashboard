
# # backend/app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_bcrypt import Bcrypt
from clickhouse_driver import Client as ClickHouseClient
from flask_mail import Mail
from config import Config
from flask_migrate import Migrate

# Global extension instances (only one of each!)
db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()
bcrypt = Bcrypt()
mail = Mail()
migrate = Migrate()
clickhouse_client = None  # will be set in create_app

def create_app(config_class=Config):
    app = Flask(__name__)
    # app.config.from_object(config_class)
    app.config.from_object("config.Config")

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cache.init_app(app, config={
        "CACHE_TYPE": "RedisCache",
        "CACHE_REDIS_URL": app.config.get("REDIS_URL")
    })
    bcrypt.init_app(app)
    mail.init_app(app)

    # Init ClickHouse
    global clickhouse_client
    try:
        clickhouse_client = ClickHouseClient.from_url(
            app.config.get("CLICKHOUSE_DATABASE_URI")
        )
    except Exception:
        clickhouse_client = None

    # Register blueprints
    from app.api.routes import api_bp
    from app.auth.routes import auth_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app


