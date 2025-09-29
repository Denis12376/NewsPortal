import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'post-views-every-week': {
        'task': 'news.tasks.send_weekly_digest',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),
        'args': ()
    }
}

app.conf.task_routes = {
    'news.tasks.send_post_notifications_task': {'queue': 'celery'},
    'news.tasks.send_weekly_digest': {'queue': 'celery'},
}