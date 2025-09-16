# backend/app/auth/routes.py

from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        #  Access token with role + region claims
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "username": user.username,
                "role": user.role,
                "region": getattr(user, "region", "all")
            }
        )

        #  Refresh token only carries user.id
        refresh_token = create_refresh_token(identity=str(user.id))

        return jsonify(
            access_token=access_token,
            refresh_token=refresh_token,
            role=user.role,
            region=user.region
        )

    return jsonify({"msg": "Invalid credentials"}), 401


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()  # string user.id
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({"msg": "User not found"}), 404

    new_access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "username": user.username,
            "role": user.role,
            "region": getattr(user, "region", "all")
        }
    )
    new_refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        role=user.role,
        region=user.region
    ), 200
