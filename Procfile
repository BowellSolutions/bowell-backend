release: python manage.py makemigrations --settings=core.settings.heroku --no-input && python manage.py migrate --settings=core.settings.heroku --no-input
web: daphne core.asgi:application -b 0.0.0.0 -p $PORT
worker: celery worker -A analysis -l INFO"
