import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_REDIS_URL = "redis://redis:6379/0"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    CHATWORK_API_TOKEN = os.environ.get("CHATWORK_API_TOKEN", "")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    CHATWORK_WEBHOOK_TOKEN = os.environ.get("CHATWORK_WEBHOOK_TOKEN", "")
    CHATWORK_WEBHOOK_ID = os.environ.get("CHATWORK_WEBHOOK_ID", "")

    # Celery configurations
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL") or DEFAULT_REDIS_URL
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND") or DEFAULT_REDIS_URL

    # Add these lines to the Config class
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
    GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "owner/repo")
    GITHUB_EXCLUDE_PATTERNS = os.environ.get("GITHUB_EXCLUDE_PATTERNS", "")

    # https://www.reddit.com/r/flask/comments/1z1oox/af_flasksqlalchemy_has_a_parameter_sqlalchemy/
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False

    # https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 1800
    CACHE_REDIS_URL = os.environ.get("CACHE_REDIS_URL") or DEFAULT_REDIS_URL

    # Connection to database
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    database_name = os.getenv("SQLITE_DATABASE_NAME", default="database.db")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, database_name)}"


class ProductionConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False


class DevelopmentConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
