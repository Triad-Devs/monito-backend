web: python manage.py makemigrations && python manage.py migrate && gunicorn monito.wsgi 
celery: celery -A monito.celery worker --pool=solo -l info
celerybeat: celery -A monito beat -l INFO
