from src.main import create_app, create_celery_app
from src.utils.logger import logger

app = create_app()
celery_app = create_celery_app(app)


if __name__ == "__main__":

    logger.info("Starting the application in debug mode with auto-reloading")
    app.run(
        host="0.0.0.0",
        port=app.config["PORT"],
        debug=True,
        use_reloader=True,
    )
