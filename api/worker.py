import os
from celery import Celery


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
RESULT_BACKEND = os.environ.get('RESULT_BACKEND')


celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=RESULT_BACKEND)
