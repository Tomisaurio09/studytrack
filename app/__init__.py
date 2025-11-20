import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from .config import DevConfig, TestConfig, ProdConfig

db = SQLAlchemy()
migrate = Migrate()
api = Api(spec_kwargs={
    "title": "StudyTrack API",
    "version": "1.0.0",
    "openapi_version": "3.0.3",
})
jwt = JWTManager()


def create_app(env="development"):
    app = Flask(__name__)

    if env == "production":
        app.config.from_object(ProdConfig)
    elif env == "testing":
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(DevConfig)

    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize flask-smorest API (handles OpenAPI/Swagger)
    api.init_app(app)
    
    # Initialize JWT manager for token creation/validation
    jwt.init_app(app)
    
    # Initialize limiter BEFORE importing routes (so @limiter.limit decorators work)
    from app.utils.limiters import limiter
    limiter.init_app(app)
    
    # Register blueprints with the API
    try:
        from app.routes.auth_routes import auth_bp
        api.register_blueprint(auth_bp)
        from app.routes.subject_routes import subject_bp
        api.register_blueprint(subject_bp)
        from app.routes.study_sessions_routes import study_sessions_bp
        api.register_blueprint(study_sessions_bp)
    except Exception as e:
        # Print error so it's visible (instead of silently failing)
        print(f"Error registering blueprints: {e}")
        import traceback
        traceback.print_exc()

    return app


