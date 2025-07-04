from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_parser_and_job_matcher.settings')
app = Celery('parser_and_job_matcherapp',
                broker='redis://',
                inclue=['parser_and_job_matcherapp.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-weekly-emails': {
        'task': 'parser_and_job_matcherapp.tasks.send_weekly_job_match_emails',
        'schedule': crontab(minute='*'),  
    },
}