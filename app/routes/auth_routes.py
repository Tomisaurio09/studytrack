from flask import request, jsonify
from app.models import User
from app import db
from flask_smorest import Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token
from flask.views import MethodView
from app.schemas.user_schema import RegisterSchema, LoginSchema
from app.utils.limiters import limiter
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

auth_bp = Blueprint("auth", "auth", url_prefix="/auth")


@auth_bp.route("/register")
class RegisterResource(MethodView):
    @auth_bp.arguments(RegisterSchema)
    @auth_bp.response(201)
    @limiter.limit("10 per minute")
    def post(self, user_data):
        if User.query.filter_by(username=user_data["username"]).first():
            logging.error(f"Registration error: Username '{user_data['username']}' already exists")
            return {"error": "This username already exists"}, 400
        if User.query.filter_by(email=user_data["email"]).first():
            logging.error(f"Registration error: Email '{user_data['email']}' already in use")
            return {"error": "This email is already in use"}, 400

        new_user = User(
            username=user_data["username"],
            email=user_data["email"]
        )
        new_user.set_password(user_data["password"])

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating user: {e}")
            return {"error": "An error occurred while creating the user"}, 500

        logging.info(f"A new user has been created. Username: '{user_data['username']}' Email: '{user_data['email']}'")
        return {"message": "User created successfully"}, 201

@auth_bp.route("/login")
class LoginResource(MethodView):
    @auth_bp.arguments(LoginSchema)
    @auth_bp.response(200)  
    @limiter.limit("10 per minute")
    def post(self, user_data):
        user = User.query.filter_by(username=user_data["username"]).first()
        if not user or not user.check_password(user_data["password"]):
            logging.warning(f"Failed login attempt for username: {user_data['username']}")
            return {"error": "Invalid username or password"}, 401

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        logging.info(
            "User login successful",
            extra={
                "user_id": user.id,
                "username": user.username}
        )
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
    
@auth_bp.route("/refresh")
class RefreshResource(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        return {"access_token": access_token}, 200