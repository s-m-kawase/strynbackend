release: python manage.py migrate
web: gunicorn stryn.wsgi --workers=3 --timeout=180 --log-file -