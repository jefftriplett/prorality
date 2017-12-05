web: python manage.py runserver
redis: redis-server
worker: celery -A config worker -l info -Ofair
beat: celery -A config beat -l info -S django
