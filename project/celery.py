from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

celery = Celery('project')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
