
# backend/app/api/routes.py

from flask import Blueprint, request, jsonify, Response, send_file
import csv
import io
import matplotlib
matplotlib.use("Agg")  # for headless/Docker
import matplotlib.pyplot as plt
from flask_jwt_extended import jwt_required, get_jwt_identity

# ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Spacer,
    Image,
    Paragraph,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# project imports
from db.clickhouse_client import fetch_region_kpis, fetch_region_product_kpis
from utils.pdf_utils import build_kpi_table, build_product_table
from tasks import generate_region_pdf

api_bp = Blueprint("api", __name__)

# -------------------------
# Mock fallback data
# -------------------------
MOCK_KPIS = [
    {"region": "NA", "total_sales": 5000000, "new_customers": 150, "churn_rate": 2.5},
    {"region": "EU", "total_sales": 3200000, "new_customers": 120, "churn_rate": 3.1},
    {"region": "APAC", "total_sales": 2100000, "new_customers": 90, "churn_rate": 4.0},
]

MOCK_PRODUCTS = [
    {"product_category": "Electronics", "total_sales": 1500000, "new_customers": 345, "churn_rate": 3.2},
    {"product_category": "Apparel", "total_sales": 1000000, "new_customers": 290, "churn_rate": 4.1},
    {"product_category": "Home Goods", "total_sales": 700000, "new_customers": 255, "churn_rate": 5.0},
]


def apply_date_range(data, date_range: str):
    """Simple multiplier-based mock adjustments for date ranges"""
    if date_range == "last_7_days":
        return [{**k, "total_sales": int(k["total_sales"] * 0.2)} for k in data]
    elif date_range == "last_90_days":
        return [{**k, "total_sales": int(k["total_sales"] * 1.5)} for k in data]
    elif date_range == "year_to_date":
        return [{**k, "total_sales": int(k["total_sales"] * 4)} for k in data]
    return data  # last_30_days default


# -------------------------
# Helpers
# -------------------------
def _make_chart_bytes(data, kind="bar", title="Chart", xlabel=None, ylabel=None, rotate_xticks=False):
    """
    Returns a BytesIO containing a PNG image produced by matplotlib.
    `data` is a list of dicts. For product charts expect keys:
      - product_category / region (x axis)
      - total_sales (y axis)
    """
    buf = io.BytesIO()
    if not data:
        # empty image
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.text(0.5, 0.5, "No data", ha="center", va="center")
        plt.tight_layout()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        return buf

    # Determine x and y
    # If data has 'product_category', use it; otherwise 'region'
    if "product_category" in data[0]:
        x = [d["product_category"] for d in data]
    else:
        x = [d["region"] for d in data]
    y = [d.get("total_sales", 0) for d in data]

    fig, ax = plt.subplots(figsize=(5, 3))
    if kind == "bar":
        ax.bar(x, y)
        ax.set_title(title)
        if ylabel:
            ax.set_ylabel(ylabel)
        if xlabel:
            ax.set_xlabel(xlabel)
        if rotate_xticks:
            plt.xticks(rotation=30, ha="right")
    else:  # pie
        # pie needs non-zero sum; if sum is zero show placeholder
        total = sum(y)
        if total == 0:
            ax.text(0.5, 0.5, "No data", ha="center", va="center")
        else:
            ax.pie(y, labels=x, autopct="%1.1f%%", startangle=140)
            ax.set_title(title)

    plt.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf


def _compute_insights(region_rows, product_rows):
    """
    Returns a short list of insight sentences based on the data.
    region_rows: list of dicts with region-level KPIs
    product_rows: list of dicts with product-level KPIs
    """
    insights = []

    if region_rows:
        # top region by sales and lowest churn region
        top_region = max(region_rows, key=lambda r: r["total_sales"])
        lowest_churn = min(region_rows, key=lambda r: r["churn_rate"])
        insights.append(f"{top_region['region']} leads in sales (${top_region['total_sales']:,}) and has the lowest churn rate ({lowest_churn['churn_rate']:.1f}%).")

        # region with lowest sales / highest churn
        worst_region = min(region_rows, key=lambda r: r["total_sales"])
        highest_churn = max(region_rows, key=lambda r: r["churn_rate"])
        if worst_region["region"] == highest_churn["region"]:
            insights.append(f"{worst_region['region']} has the lowest revenue and the highest churn ({highest_churn['churn_rate']:.1f}%), needs attention.")
        else:
            insights.append(f"{worst_region['region']} has the lowest revenue (${worst_region['total_sales']:,}). {highest_churn['region']} has the highest churn ({highest_churn['churn_rate']:.1f}%).")

    if product_rows:
        top_prod = max(product_rows, key=lambda p: p["total_sales"])
        insights.append(f"{top_prod['product_category']} drives the highest revenue (${top_prod['total_sales']:,}).")
        # find product with highest churn
        high_churn_prod = max(product_rows, key=lambda p: p["churn_rate"])
        insights.append(f"{high_churn_prod['product_category']} has the highest churn ({high_churn_prod['churn_rate']:.1f}%).")

    return insights


# -------------------------------
# KPI Summary (JSON)
# -------------------------------
@api_bp.route("/kpi-summary", methods=["GET"])
def get_kpi_summary():
    date_range = request.args.get("dateRange", "last_30_days")
    region = request.args.get("region", "all")
    data = MOCK_KPIS if region == "all" else [k for k in MOCK_KPIS if k["region"] == region]
    data = apply_date_range(data, date_range)
    return jsonify(data)


# -------------------------------
# CSV Export
# -------------------------------
@api_bp.route("/export-csv", methods=["GET"])
def export_csv():
    date_range = request.args.get("dateRange", "last_30_days")
    region = request.args.get("region", "all")
    data = MOCK_KPIS if region == "all" else [k for k in MOCK_KPIS if k["region"] == region]
    data = apply_date_range(data, date_range)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["region", "total_sales", "new_customers", "churn_rate"])
    writer.writeheader()
    writer.writerows(data)

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=kpi_export.csv"
    return response


# -------------------------------
# Manager PDF (high-level summary + executive summary + tables + charts)
# -------------------------------
@api_bp.route("/generate-pdf", methods=["GET"])
@jwt_required()
def generate_pdf():
    """
    Manager on-demand PDF. Produces:
      - Executive summary page (Top KPIs + short insights)
      - Detailed tables + top product categories + charts
    """
    identity = get_jwt_identity()

    # Accept a region param or fall back to user's region if stored in JWT identity
    if isinstance(identity, dict):
        default_region = identity.get("region", "all")
    else:
        default_region = "all"
    region = request.args.get("region", default_region)
    date_range = request.args.get("dateRange", "last_30_days")

    # Get region-level KPIs (live from ClickHouse or fallback)
    try:
        region_data = fetch_region_kpis(region, date_range=date_range)
    except Exception as e:
        print(f"❌ ClickHouse error (manager region): {e}")
        region_data = []
    if not region_data:
        region_data = MOCK_KPIS if region == "all" else [k for k in MOCK_KPIS if k["region"] == region]
        region_data = apply_date_range(region_data, date_range)

    # Get product drill-down
    try:
        product_data = fetch_region_product_kpis(region, date_range=date_range)
    except Exception as e:
        print(f"❌ ClickHouse error (manager product): {e}")
        product_data = []
    if not product_data:
        product_data = MOCK_PRODUCTS[:5]

    # Compute insights
    insights = _compute_insights(region_data, product_data)

    # Build charts (bytes)
    pie_buf = _make_chart_bytes(product_data[:3], kind="pie", title="Top 3 Categories (Share)")
    bar_buf = _make_chart_bytes(product_data[:5], kind="bar", title="Top 5 Categories (Sales)", rotate_xticks=True)

    # Build PDF document (Platypus)
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Executive summary page
    elements.append(Paragraph(f"Executive Summary - {region}", styles["Title"]))
    elements.append(Spacer(1, 0.15 * inch))

    # Top KPI highlights (take first region row if region-specific; or aggregated)
    if region_data:
        # If region_data is multiple regions (region == "all"), summarize totals
        if region == "all":
            total_sales_total = sum(r["total_sales"] for r in region_data)
            total_new_customers = sum(r["new_customers"] for r in region_data)
            avg_churn = sum(r["churn_rate"] for r in region_data) / len(region_data)
            highlights_text = f"<b>Total Sales:</b> ${total_sales_total:,}<br/><b>New Customers:</b> {total_new_customers}<br/><b>Average Churn Rate:</b> {avg_churn:.2f}%"
        else:
            s = region_data[0]
            highlights_text = f"<b>Total Sales:</b> ${s['total_sales']:,}<br/><b>New Customers:</b> {s['new_customers']}<br/><b>Churn Rate:</b> {s['churn_rate']:.2f}%"
    else:
        highlights_text = "<b>Total Sales:</b> $0<br/><b>New Customers:</b> 0<br/><b>Churn Rate:</b> 0%"

    elements.append(Paragraph(highlights_text, styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))

    # Add insights bullets
    if insights:
        insights_html = "<br/>".join([f"• {i}" for i in insights])
        elements.append(Paragraph("<b>Insights:</b>", styles["Heading2"]))
        elements.append(Paragraph(insights_html, styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

    # Quick pie chart (top 3)
    elements.append(Image(pie_buf, width=320, height=200))
    elements.append(PageBreak())

    # Detailed report page(s)
    elements.append(Paragraph(f"Weekly KPI Report - {region}", styles["Heading1"]))
    elements.append(Spacer(1, 0.12 * inch))

    elements.append(Paragraph("Regional Performance", styles["Heading2"]))
    elements.append(build_kpi_table(region_data))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("Top Product Categories", styles["Heading2"]))
    elements.append(build_product_table(product_data))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("Category Charts", styles["Heading2"]))
    elements.append(Image(bar_buf, width=420, height=250))
    elements.append(Spacer(1, 0.12 * inch))

    # Finalize
    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="manager_report.pdf", mimetype="application/pdf")


# -------------------------------
# Analyst PDF (detailed drill-down)
# -------------------------------
@api_bp.route("/export-pdf", methods=["GET"])
@jwt_required()
def export_pdf():
    """
    Analyst on-demand PDF: filtered KPI report with tables + product drill-down + charts.
    """
    identity = get_jwt_identity()
    date_range = request.args.get("dateRange", "last_30_days")
    region = request.args.get("region", "all")

    # Region summary
    try:
        region_data = fetch_region_kpis(region, date_range=date_range)
    except Exception as e:
        print(f"❌ ClickHouse error (analyst region): {e}")
        region_data = []
    if not region_data:
        region_data = MOCK_KPIS if region == "all" else [k for k in MOCK_KPIS if k["region"] == region]
        region_data = apply_date_range(region_data, date_range)

    # Product drill-down
    try:
        product_data = fetch_region_product_kpis(region, date_range=date_range)
    except Exception as e:
        print(f"❌ ClickHouse error (analyst product): {e}")
        product_data = []
    if not product_data:
        product_data = MOCK_PRODUCTS

    # Build charts
    bar_buf = _make_chart_bytes(product_data, kind="bar", title=f"Top Product Categories ({date_range})", rotate_xticks=True)
    pie_buf = _make_chart_bytes(product_data, kind="pie", title=f"Product Share ({date_range})")

    # Build PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Filtered KPI Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.12 * inch))

    elements.append(Paragraph("Region Summary", styles["Heading2"]))
    elements.append(build_kpi_table(region_data))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("Top Product Categories", styles["Heading2"]))
    elements.append(build_product_table(product_data))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("Category Charts", styles["Heading2"]))
    elements.append(Image(bar_buf, width=420, height=250))
    elements.append(Spacer(1, 0.12 * inch))
    elements.append(Image(pie_buf, width=420, height=250))

    doc.build(elements)
    buffer.seek(0)  
    return send_file(buffer, as_attachment=True, download_name="filtered_report.pdf", mimetype="application/pdf")
