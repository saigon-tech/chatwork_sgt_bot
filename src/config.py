import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    APP_PORT = os.environ.get("APP_PORT") or 5000
    CHATWORK_API_TOKEN = os.environ.get("CHATWORK_API_TOKEN")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    CHATWORK_WEBHOOK_TOKEN = os.environ.get("CHATWORK_WEBHOOK_TOKEN")
    CHATWORK_WEBHOOK_ID = os.environ.get("CHATWORK_WEBHOOK_ID")

    # Celery configurations
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL") or "redis://redis:6379/0"
    CELERY_RESULT_BACKEND = (
        os.environ.get("CELERY_RESULT_BACKEND") or "redis://redis:6379/0"
    )
