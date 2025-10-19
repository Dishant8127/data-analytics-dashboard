from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors
from db.clickhouse_client import fetch_region_kpis, fetch_region_product_kpis


def generate_region_pdf(manager):
    """
    Generate a PDF report for a given manager's region.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # ✅ Title
    elements.append(Paragraph(f"Weekly KPI Report - {manager.region}", styles["Heading1"]))
    elements.append(Spacer(1, 12))

    # ✅ Fetch region KPIs
    region_data = fetch_region_kpis(manager.region, date_range="last_7_days")
    if region_data:
        elements.append(Paragraph("Regional KPIs", styles["Heading2"]))
        table_data = [["Region", "Total Sales", "New Customers", "Churn Rate (%)"]]
        for row in region_data:
            table_data.append([
                row["region"],
                f"{row['total_sales']:.2f}",
                str(row["new_customers"]),
                f"{row['churn_rate']:.2f}"
            ])
        t = Table(table_data, hAlign="LEFT")
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 24))

    # ✅ Fetch product KPIs
    product_data = fetch_region_product_kpis(manager.region, date_range="last_7_days")
    if product_data:
        elements.append(Paragraph("Top Product Categories", styles["Heading2"]))
        table_data = [["Product Category", "Total Sales", "New Customers", "Churn Rate (%)"]]
        for row in product_data:
            table_data.append([
                row["product_category"],
                f"{row['total_sales']:.2f}",
                str(row["new_customers"]),
                f"{row['churn_rate']:.2f}"
            ])
        t = Table(table_data, hAlign="LEFT")
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t)

    # ✅ Build and return
    doc.build(elements)
    buffer.seek(0)
    return buffer
