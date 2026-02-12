from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import ssl
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'liture.settings')

app = Celery('liture')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
