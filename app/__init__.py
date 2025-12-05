from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from .config import DevConfig, TestConfig, ProdConfig
import logging
from flask_caching import Cache
from flask_cors import CORS
from app.utils.middleware import enforce_allowed_hosts




db = SQLAlchemy()
migrate = Migrate()
api = Api(spec_kwargs={
    "title": "StudyTrack API",
    "version": "1.0.0",
    "openapi_version": "3.0.3",
})
jwt = JWTManager()
cache = Cache()


def create_app(env="development"):
    app = Flask(__name__)

    if env == "production":
        app.config.from_object(ProdConfig)
    elif env == "testing":
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(DevConfig)

    app.config["API_TITLE"] = "StudyTrack API"
    app.config["API_VERSION"] = "1.0.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"  
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    CORS(
        app,
        origins=["https://studytrack.com"],
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Content-Type", "Authorization"],
    )
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

    enforce_allowed_hosts(app)
    from app.utils.limiters import limiter
    limiter.init_app(app)

    if app.debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s in %(module)s: %(message)s',
            handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()  
        ]
        )


    try:
        from app.routes.auth_routes import auth_bp
        api.register_blueprint(auth_bp)
        from app.routes.subject_routes import subject_bp
        api.register_blueprint(subject_bp)
        from app.routes.study_sessions_routes import study_sessions_bp
        api.register_blueprint(study_sessions_bp)
    except Exception as e:
        print(f"Error registering blueprints: {e}")
        import traceback
        traceback.print_exc()

    from app.utils.error_handler import register_error_handlers
    register_error_handlers(app)
    
    return app


