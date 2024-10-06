web: gunicorn run:app --bind 0.0.0.0:$PORT
worker: sh -c 'chmod +x entrypoint.sh && entrypoint.sh && celery -A run.celery_app worker -l info'
