
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










# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager
# from flask_caching import Cache
# from flask_bcrypt import Bcrypt
# from clickhouse_driver import Client as ClickHouseClient
# from flask_mail import Mail
# from config import Config

# # extension instances (import these from other modules)
# db = SQLAlchemy()
# jwt = JWTManager()
# cache = Cache()
# bcrypt = Bcrypt()
# clickhouse_client = None  # will be set in create_app
# Mail = Mail()

# def create_app(config_class=Config):
#     app = Flask(__name__, instance_relative_config=False)
#     app.config.from_object(config_class)

#     # init extensions
#     db.init_app(app)
#     jwt.init_app(app)
#     cache.init_app(app, config={"CACHE_TYPE": "RedisCache", "CACHE_REDIS_URL": app.config.get("REDIS_URL")})
#     bcrypt.init_app(app)
#     Mail.init_app(app)

#     # init clickhouse client (store globally in this module)
#     global clickhouse_client
#     try:
#         clickhouse_client = ClickHouseClient.from_url(app.config.get("CLICKHOUSE_DATABASE_URI"))
#     except Exception:
#         clickhouse_client = None

#     # register blueprints (use package imports)
#     from backend.app.api.routes import api_bp
#     from backend.app.auth.routes import auth_bp

#     app.register_blueprint(api_bp, url_prefix="/api")
#     app.register_blueprint(auth_bp, url_prefix="/auth")

#     @app.route("/health")
#     def health():
#         return {"status": "ok"}

#     return app





















# # app/__init__.py
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager
# from backend.config import Config  # Import Config class

# db = SQLAlchemy()
# bcrypt = Bcrypt()
# jwt = JWTManager()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)  # Load all configurations from Config class

#     db.init_app(app)
#     bcrypt.init_app(app)
#     jwt.init_app(app)
    

#     from .auth.routes import auth_bp
#     from .api.routes import api_bp

#     app.register_blueprint(auth_bp, url_prefix="/auth")
#     app.register_blueprint(api_bp, url_prefix="/api")

#     return app