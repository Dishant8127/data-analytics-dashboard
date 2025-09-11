
from celery import Celery
import os

def make_celery():
    broker = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    backend = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    celery = Celery("tasks", broker=broker, backend=backend, include=["tasks"])  # ✅ include tasks
    return celery

celery = make_celery()

