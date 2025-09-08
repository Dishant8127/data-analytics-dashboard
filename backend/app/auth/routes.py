# backend/app/auth/routes.py




from flask import Blueprint, request, jsonify
from app.models import User
from app import db, bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role": user.role
        }), 200

    return jsonify({"msg": "Invalid username or password"}), 401



