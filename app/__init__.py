import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import DevConfig, TestConfig, ProdConfig

db = SQLAlchemy()
migrate = Migrate()

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

    return app

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import DevConfig, TestConfig, ProdConfig

db = SQLAlchemy()
migrate = Migrate()

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

    return app
