from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from datetime import timedelta
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KETEP_DashBoard.settings')

app = Celery('KETEP_DashBoard', broker='amqp://guest:guest@localhost:5672//')
# app = Celery('KETEP_DashBoard')
# v4.0 이상 일 경우
# app.config_from_object('django.conf:settings', namespace='CELERY')
# v3.1 일 경우
app.config_from_object('django.conf:settings')

# v4.0 이상 일 경우
# app.autodiscover_tasks()
# v3.1 일 경우
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
    CELERYBEAT_SCHEDULE = {
        'say_hello-every-seconds': {
            # 'task': 'energy.tasks.say_hello',
            'task': 'energy.tasks.say_hello',
            'schedule': timedelta(seconds=10),
            'args': ()
        },
    }
)

# app.conf.update(
#     CELERY_TASK_RESULT_EXPIRES=3600,
# )
#
# if __name__ == '__main__':
#     app.start()