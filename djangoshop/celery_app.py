import os
import time

from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from shopapp.tasks import test_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoshop.settings')

app = Celery('djangoshop')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()

@app.task()
def debug_task():
    time.sleep(10)
    print('ended debug task')

# need to restart sheduler if task has changed
app.conf.beat_schedule = {
    'add-every-minute': {
        'task': 'shopapp.tasks.test_task',
        'schedule': crontab(minute='*/1'),
        'args': ('first arg', 'second arg'),
    },
}