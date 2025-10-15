import io
from celery import Celery
from reportlab.platypus import SimpleDocTemplate, Spacer, Image, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from utils.pdf_utils import (
    build_kpi_table,
    build_product_table,
    build_product_chart,
    build_trend_table,
)
from db.clickhouse_client import (
    fetch_region_kpis,
    fetch_region_product_kpis,
    fetch_region_kpi_trends,
)
from utils.kpi_utils import calc_trend


# ======================================================
# Celery configuration
# ======================================================
celery = Celery("tasks", broker="redis://redis:6379/0")


# ======================================================
# Helper: generate Region PDF for Managers
# ======================================================
def generate_region_pdf(manager):
    """
    Generate a Manager PDF report containing:
    - Executive summary with trend comparison (vs previous week)
    - KPI tables and charts
    - Product category breakdown
    """

    #  Fetch KPI trends (current vs previous week)
    current, previous = fetch_region_kpi_trends(manager.region, period_days=7)
    if not current:
        current = {"total_sales": 0, "new_customers": 0, "churn_rate": 0}
    if not previous:
        previous = {"total_sales": 0, "new_customers": 0, "churn_rate": 0}

    #  Fetch region summary and top product categories
    region_data = fetch_region_kpis(manager.region, date_range="last_7_days")
    if not region_data:
        region_data = [
            {
                "region": manager.region,
                "total_sales": 0,
                "new_customers": 0,
                "churn_rate": 0,
            }
        ]

    product_data = fetch_region_product_kpis(manager.region, date_range="last_7_days")
    if not product_data:
        product_data = [
            {
                "product_category": "N/A",
                "total_sales": 0,
                "new_customers": 0,
                "churn_rate": 0,
            }
        ]

    #  Create the PDF buffer and doc structure
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # ======================================================
    # EXECUTIVE SUMMARY PAGE
    # ======================================================
    elements.append(Paragraph(f"Executive Summary - {manager.region}", styles["Title"]))
    elements.append(Spacer(1, 0.2 * inch))

    # Compute trends (% changes)
    sales_trend = calc_trend(current["total_sales"], previous["total_sales"])
    cust_trend = calc_trend(current["new_customers"], previous["new_customers"])
    churn_trend = calc_trend(current["churn_rate"], previous["churn_rate"])

    summary_html = f"""
        <b>Total Sales:</b> ${current['total_sales']:,} ({sales_trend})<br/>
        <b>New Customers:</b> {current['new_customers']} ({cust_trend})<br/>
        <b>Churn Rate:</b> {current['churn_rate']:.2f}% ({churn_trend})<br/>
    """
    elements.append(Paragraph(summary_html, styles["Normal"]))
    elements.append(Spacer(1, 0.4 * inch))

    # Add Top 3 Categories Pie Chart
    pie_chart = build_product_chart(product_data[:3], chart_type="pie")
    if pie_chart:
        elements.append(Image(pie_chart, width=300, height=200))

    # Add trend comparison table
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(build_trend_table(current, previous))

    # Page break before detailed report
    elements.append(PageBreak())

    # ======================================================
    # DETAILED REPORT
    # ======================================================
    elements.append(Paragraph(f"Weekly KPI Report - {manager.region}", styles["Heading1"]))
    elements.append(Spacer(1, 0.2 * inch))

    # Region summary table
    elements.append(Paragraph("Region Summary", styles["Heading2"]))
    elements.append(build_kpi_table(region_data))
    elements.append(Spacer(1, 0.3 * inch))

    # Product table
    elements.append(Paragraph("Top 5 Product Categories", styles["Heading2"]))
    elements.append(build_product_table(product_data[:5]))
    elements.append(Spacer(1, 0.3 * inch))

    # Product charts
    elements.append(Paragraph("Category Charts", styles["Heading2"]))
    bar_chart = build_product_chart(product_data[:5], chart_type="bar")
    pie_chart = build_product_chart(product_data[:5], chart_type="pie")
    if bar_chart:
        elements.append(Image(bar_chart, width=400, height=250))
    if pie_chart:
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Image(pie_chart, width=400, height=250))

    # Build final PDF document
    doc.build(elements)
    buffer.seek(0)

    return buffer


# ======================================================
# Celery Task (optional async execution)
# ======================================================
@celery.task
def send_weekly_manager_report(manager_data):
    """
    Celery task to generate and email the weekly manager report.
    manager_data should include: { 'username': str, 'region': str, 'email': str }
    """
    class Manager:
        def __init__(self, username, region, email):
            self.username = username
            self.region = region
            self.email = email

    manager = Manager(
        username=manager_data.get("username", "Manager"),
        region=manager_data.get("region", "All"),
        email=manager_data.get("email", None),
    )

    pdf_buffer = generate_region_pdf(manager)

    # TODO: integrate email sending logic here (e.g. using smtplib or SendGrid)
    # Example:
    # send_email_with_attachment(manager.email, "Weekly KPI Report", pdf_buffer)

    print(f"✅ Weekly PDF report generated for {manager.username} ({manager.region})")

    return True
