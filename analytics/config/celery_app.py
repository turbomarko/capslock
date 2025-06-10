import os

from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("analysis")
app.config_from_object("django.conf:settings", namespace="CELERY")


@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig

    from django.conf import settings

    dictConfig(settings.LOGGING)


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Schedule the analytics task to run every day at 06:20
app.conf.beat_schedule = {
    'analyze-campaign-performance': {
        'task': 'analytics.tasks.analyze_campaign_performance',
        'schedule': crontab(minute=3),
    },
}
