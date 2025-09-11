
from celery import Celery
import os

def make_celery():
    broker = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    backend = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    celery = Celery("tasks", broker=broker, backend=backend, include=["tasks"])  # ✅ include tasks
    return celery

celery = make_celery()







# from celery import Celery
# import os

# # Redis as broker
# CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
# CELERY_BACKEND_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_BACKEND_URL)
