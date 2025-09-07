# backend/app/auth/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app.models import User  # make sure this points to your SQLAlchemy User model




auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    # Fetch user from database
    user = User.query.filter_by(username=username).first()

    # Check if user exists and password is correct
    if user and check_password_hash(user.password, password):
        # Create token (without role)
        token = create_access_token(identity={"id": user.id})
        return jsonify(access_token=token)

    return jsonify({"msg": "Invalid credentials"}), 401



