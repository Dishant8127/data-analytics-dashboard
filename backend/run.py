# run.py

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import Config
from flask_cors import CORS  # ✅ Import CORS
from sqlalchemy import text
from flask_caching import Cache
from app import db, jwt, bcrypt, create_app
# from app import create_app


# db = SQLAlchemy()
# jwt = JWTManager()
# cache = Cache(config={"CACHE_TYPE": "RedisCache", "CACHE_REDIS_URL": Config.REDIS_URL})

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Enable CORS for frontend origin
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    # cache.init_app(app)

    from app.api.routes import api_bp
    from app.auth.routes import auth_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/health")
    def health():
        try:
            result = db.session.execute(text("SELECT 1")).scalar()
            status = "connected" if result == 1 else "disconnected"
            return {"db": status, "status": "ok"}
        except Exception as e:
            return {"db": "disconnected", "error": str(e), "status": "error"}

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
