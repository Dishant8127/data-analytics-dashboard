# run.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import Config
from flask_cors import CORS
from sqlalchemy import text

# Import the extensions defined in app/__init__.py
from app import db, jwt, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for all routes and origins (for development purposes)
    CORS(app, resources={r"/*": {"origins": "*"}})
    # CORS(app, resources={r"/auth/*": {"origins": "http://localhost:5173"}})


    # Initialize Flask extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Register Blueprints
    from app.api.routes import api_bp
    from app.auth.routes import auth_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Health check route to ensure DB connectivity
    @app.route("/health")
    def health():
        try:
            result = db.session.execute(text("SELECT 1")).scalar()
            status = "connected" if result == 1 else "disconnected"
            return {"db": status, "status": "ok"}
        except Exception as e:
            return {"db": "disconnected", "error": str(e), "status": "error"}

    return app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    # Run the app on localhost port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
