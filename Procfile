web: python manage.py makemigrations && python manage.py migrate && gunicorn monito.wsgi 
worker: celery -A monito.celery worker --pool=solo -l info & celery -A monito beat -l INFO
