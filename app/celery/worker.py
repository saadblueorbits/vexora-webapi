import time
# from celery import Celery
from .app import celery_app

@celery_app.task(name="create_task")
def create_task(task_type):
    print("===============================CELERY TASK==========================================")
    time.sleep(int(task_type) * 10)
    return True