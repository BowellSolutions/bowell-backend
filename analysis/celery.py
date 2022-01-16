"""
author: Gustaw Daczkowski

description: Celery application setup.
"""
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')

app = Celery('analysis')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
