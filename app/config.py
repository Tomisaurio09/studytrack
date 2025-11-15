import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL",
        "sqlite:///dev.db"
    )


class TestConfig(Config):
    DEBUG = False
    TESTING = True
    ENV = "testing"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "sqlite:///test.db"
    )


class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    ENV = "production"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "PROD_DATABASE_URL",
        "sqlite:///prod.db"
    )

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL",
        "sqlite:///dev.db"
    )


class TestConfig(Config):
    DEBUG = False
    TESTING = True
    ENV = "testing"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "sqlite:///test.db"
    )


class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    ENV = "production"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "PROD_DATABASE_URL",
        "sqlite:///prod.db"
    )

