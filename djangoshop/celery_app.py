import os
import time

from django.core.mail import send_mail
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoshop.settings')

app = Celery('djangoshop')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()

@app.task()
def debug_task():
    time.sleep(10)
    print('ended task')

@app.task()# launch delayed task in signals
def send_order_mail():
    send_mail('Subject here',
    'Here is the message.',
    'djangoshop@app.com',
    ['user@email'],
    fail_silently=False,)