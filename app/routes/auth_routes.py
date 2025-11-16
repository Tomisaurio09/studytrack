from flask import request, jsonify
from app.models.users import User
from app import db
from flask_smorest import Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token
from flask.views import MethodView
from app.schemas.user_schema import RegisterSchema, LoginSchema

auth_bp = Blueprint("auth", "auth", url_prefix="/auth")


@auth_bp.route("/register")
class RegisterResource(MethodView):
    @auth_bp.arguments(RegisterSchema)
    @auth_bp.response(201)
    def post(self, user_data):
        if User.query.filter_by(username=user_data["username"]).first():
            return {"error": "Ese nombre de usuario ya está en uso"}, 400
        if User.query.filter_by(email=user_data["email"]).first():
            return {"error": "Ese email ya está en uso"}, 400

        new_user = User(
            username=user_data["username"],
            email=user_data["email"]
        )
        new_user.set_password(user_data["password"])

        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=str(new_user.id))
        refresh_token = create_refresh_token(identity=str(new_user.id))

        return jsonify({
            "message": "Usuario creado con éxito",
            "access_token": access_token,
            "refresh_token": refresh_token
        })

@auth_bp.route("/login")
class LoginResource(MethodView):
    @auth_bp.arguments(LoginSchema)
    @auth_bp.response(201)
    def post(self, user_data):
        user = User.query.filter_by(username=user_data["username"]).first()
        if user and user.check_password(user_data["password"]):
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))

            return jsonify({
                "message": "Inicio de sesión exitoso",
                "access_token": access_token,
                "refresh_token": refresh_token
            })