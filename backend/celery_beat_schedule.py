
from celery_worker import celery
from celery.schedules import crontab

# Example: send every Monday at 9 AM
celery.conf.beat_schedule = {
    "send-weekly-reports": {
        "task": "tasks.send_weekly_reports",
        "schedule": crontab(hour=9, minute=0, day_of_week="monday"),
    },
}
