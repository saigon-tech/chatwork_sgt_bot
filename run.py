from src.main import create_app, create_celery_app

app = create_app()
celery_app = create_celery_app(app)

if __name__ == "__main__":
    # Run in local
    app.run(host='0.0.0.0', port=app.config['APP_PORT'], debug=app.debug)
