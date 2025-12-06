import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", "False") == "True"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    CACHE_REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
    CACHE_REDIS_DB = int(os.environ.get("REDIS_DB", 0))
    CACHE_REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
class DevConfig(Config):
    DEBUG = os.environ.get("DEBUG", "True") == "True"
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL",
        "sqlite:///dev.db"
    )
    CACHE_TYPE = "SimpleCache"


class TestConfig(Config):
    DEBUG = os.environ.get("DEBUG", "False") == "True"
    TESTING = True
    ENV = "testing"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "sqlite:///test.db"
    )
    CACHE_TYPE = "SimpleCache"


class ProdConfig(Config):
    DEBUG = os.environ.get("DEBUG", "False") == "True"
    TESTING = False
    ENV = "production"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///prod.db"
    )

