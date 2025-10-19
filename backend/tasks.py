from celery import Celery
from flask_mail import Message
from utils.report_generation import generate_region_pdf
from app.models import User
from app import mail, create_app

celery = Celery(__name__)
celery.conf.broker_url = "redis://redis:6379/0"

app = create_app()

@celery.task
def send_weekly_reports():
    with app.app_context():
        managers = User.query.filter_by(role="manager").all()
        for manager in managers:
            pdf_buffer = generate_region_pdf(manager)
            msg = Message("Weekly KPI Report", recipients=[manager.email])
            msg.body = f"Hello {manager.username}, attached is your weekly KPI report for {manager.region}."
            msg.attach("weekly_report.pdf", "application/pdf", pdf_buffer.getvalue())
            mail.send(msg)
    return "Reports emailed successfully."
