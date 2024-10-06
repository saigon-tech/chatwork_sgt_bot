web: gunicorn run:app --bind 0.0.0.0:$PORT
worker: sh -c 'chmod +x /home/user/sgtbot/entrypoint.sh && /home/user/sgtbot/entrypoint.sh && celery -A run.celery_app worker -l info'
