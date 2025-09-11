


from celery_worker import celery
from flask_mail import Message
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt

from app import create_app, db, mail
from app.models import User

# Create Flask app for Celery
flask_app = create_app()

def build_pdf(username):
    """Generate PDF with a chart"""
    fig, ax = plt.subplots(figsize=(4, 2.4))
    regions = ["NA", "EU", "APAC"]
    sales = [5000000, 3200000, 2100000]
    ax.bar(regions, sales)
    ax.set_title("Sales by Region")
    plt.tight_layout()

    chart_buf = io.BytesIO()
    plt.savefig(chart_buf, format="png", bbox_inches="tight")
    plt.close(fig)
    chart_buf.seek(0)
    chart_img = ImageReader(chart_buf)

    pdf_buf = io.BytesIO()
    c = canvas.Canvas(pdf_buf, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Weekly KPI Report")
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, f"Hello {username}, here is your weekly KPI report.")
    c.drawImage(chart_img, 100, 420, width=360, height=200)
    c.showPage()
    c.save()
    pdf_buf.seek(0)
    return pdf_buf

@celery.task
def send_weekly_reports():
    """Celery task to email all managers"""
    with flask_app.app_context():
        managers = User.query.filter_by(role="manager").all()

        for manager in managers:
            pdf_buf = build_pdf(manager.username)

            msg = Message(
                subject="Weekly KPI Report",
                recipients=[manager.email],
                body=f"Hi {manager.username},\n\nAttached is your weekly KPI report."
            )
            msg.attach("weekly_report.pdf", "application/pdf", pdf_buf.read())
            mail.send(msg)

        return f"✅ Sent reports to {[m.email for m in managers]}"
