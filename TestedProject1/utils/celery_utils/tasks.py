from .email_tasks import *
from celery import shared_task

@shared_task
def ping():
    return 'pong'