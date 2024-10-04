from flask import Flask
from celery import Celery
from src.api.routes import api_bp
from .extensions import db, migrate

# flake8: noqa
import src.model


def create_app(setting_override=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("src.config.Config")
    if setting_override:
        app.config.update(setting_override)

    app.register_blueprint(api_bp)
    extensions(app)

    @app.route("/")
    def index():
        return "It works!"

    return app


def create_celery_app(app=None):
    app = app or create_app()
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def extensions(app):
    db.init_app(app)
    migrate.init_app(app)
