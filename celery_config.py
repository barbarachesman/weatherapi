import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cnab_reader.settings')

celery = Celery('tasks')
celery.config_from_object('django.conf:settings')
celery.autodiscover_tasks()
