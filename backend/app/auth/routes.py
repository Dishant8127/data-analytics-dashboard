# backend/app/auth/routes.py




from flask import Blueprint, request, jsonify
from app.models import User
from app import db, bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token ,jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        # ✅ Create both access & refresh tokens
        access_token = create_access_token(identity={"id": user.id, "role": user.role})
        refresh_token = create_refresh_token(identity={"id": user.id, "role": user.role})
        return jsonify(access_token=access_token, refresh_token=refresh_token, role=user.role)
    return jsonify({"msg": "Invalid credentials"}), 401


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)  # ✅ Requires refresh token
def refresh():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    new_refresh_token = create_refresh_token(identity=identity)

    return jsonify(access_token=new_access_token,
                   refresh_token=new_refresh_token,
                   role=User.role
                   )
    

