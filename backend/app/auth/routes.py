from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import bcrypt, db
from app.models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        token = create_access_token(identity={"id": user.id, "role": user.role})
        return jsonify(access_token=token, role=user.role)  # ✅ include role
    return jsonify({"msg": "Invalid credentials"}), 401

