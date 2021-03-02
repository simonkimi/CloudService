from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloudService.settings')
app = Celery()
app.config_from_object('asynchronous.config')
