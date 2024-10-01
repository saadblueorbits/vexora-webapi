from celery import Celery
from app.config import settings

celery_app = Celery(
    broker_url = settings.CELERY_BROKER_URL,
    result_backend = settings.CELERY_RESULT_BACKEND,
    task_serializer = 'json',
    result_serializer = 'json',
    accept_content = ['json'],
    include=["app.celery.worker"],
    broker_transport_options={
        'max_retries': 1,
        'visibility_timeout': 365*24*60*60,
    }
)