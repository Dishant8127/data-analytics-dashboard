
# backend/utils/pdf_utils.py
import io
import matplotlib.pyplot as plt
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

# -------------------------
# Helper: safe formatting
# -------------------------
def _fmt_money(v):
    try:
        return f"${int(v):,}"
    except Exception:
        return f"${v}"

def _fmt_pct(v):
    try:
        return f"{float(v):.2f}%"
    except Exception:
        return f"{v}"

def _calc_trend(current, previous):
    """
    Return percentage change string and numeric (for possible coloring/logic).
    If previous is zero or missing, returns "N/A" and None.
    """
    try:
        if previous is None or previous == 0:
            return "N/A", None
        change = ((current - previous) / previous) * 100.0
        return f"{change:+.1f}%", change
    except Exception:
        return "N/A", None

# ======================================================
# KPI TABLE (Region Summary)
# ======================================================
def build_kpi_table(data):
    """
    data: list of dicts like:
      [{"region":"NA","total_sales":5000000,"new_customers":1234,"churn_rate":4.2}, ...]
    Returns a ReportLab Table object.
    """
    table_data = [["Region", "Total Sales", "New Customers", "Churn Rate (%)"]]

    for k in data:
        table_data.append([
            k.get("region", "N/A"),
            _fmt_money(k.get("total_sales", 0)),
            k.get("new_customers", 0),
            f"{k.get('churn_rate', 0):.2f}"
        ])

    table = Table(table_data, colWidths=[100, 120, 120, 120])
    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
    ])
    table.setStyle(style)
    return table

# ======================================================
# PRODUCT TABLE (Drill-Down)
# ======================================================
def build_product_table(data):
    """
    data: list of dicts:
      [{"product_category":"Electronics","total_sales":500000,"new_customers":234,"churn_rate":3.1}, ...]
    """
    table_data = [["Category", "Total Sales", "New Customers", "Churn Rate (%)"]]

    for k in data:
        table_data.append([
            k.get("product_category", "N/A"),
            _fmt_money(k.get("total_sales", 0)),
            k.get("new_customers", 0),
            f"{k.get('churn_rate', 0):.2f}"
        ])

    table = Table(table_data, colWidths=[140, 120, 120, 120])
    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
    ])
    table.setStyle(style)
    return table

# ======================================================
# PRODUCT CHART (BAR/PIE)
# ======================================================
def build_product_chart(product_data, chart_type="bar"):
    """
    product_data: list of dicts with keys 'product_category' and 'total_sales'
    chart_type: 'bar' or 'pie'
    Returns a ReportLab ImageReader object (or None if no data)
    """
    if not product_data:
        return None

    categories = [p.get("product_category", "N/A") for p in product_data]
    sales = [p.get("total_sales", 0) or 0 for p in product_data]

    fig, ax = plt.subplots(figsize=(5, 3))
    try:
        if chart_type == "bar":
            ax.bar(categories, sales, color="lightblue")
            ax.set_title("Top Product Categories (Bar)")
            ax.set_ylabel("Total Sales")
            ax.set_xlabel("Category")
            plt.xticks(rotation=30, ha="right")
        elif chart_type == "pie":
            if sum(sales) == 0:
                # avoid zero-sum pie error
                sales = [1] * len(sales)
            ax.pie(sales, labels=categories, autopct="%1.1f%%", startangle=140)
            ax.set_title("Top Product Categories (Pie)")
        plt.tight_layout()
        chart_buffer = io.BytesIO()
        plt.savefig(chart_buffer, format="png", dpi=150)
    finally:
        plt.close(fig)

    chart_buffer.seek(0)
    return ImageReader(chart_buffer)

# ======================================================
# TREND TABLE (Current vs Previous)
# ======================================================
def build_trend_table(current_metrics: dict, previous_metrics: dict):
    """
    Build a small table that shows current vs previous values and % change.

    current_metrics and previous_metrics are dicts with keys e.g.:
      {
        "total_sales": 3200000,
        "new_customers": 890,
        "churn_rate": 4.25
      }
    Returns a ReportLab Table object.
    """
    # Ensure safe defaults
    cur = current_metrics or {}
    prev = previous_metrics or {}

    rows = [
        ["Metric", "Current", "Previous", "Change"],
    ]

    # Total sales
    cur_sales = cur.get("total_sales", 0)
    prev_sales = prev.get("total_sales", 0)
    sales_change_str, _ = _calc_trend(cur_sales, prev_sales)
    rows.append(["Total Sales", _fmt_money(cur_sales), _fmt_money(prev_sales), sales_change_str])

    # New customers
    cur_cust = cur.get("new_customers", 0)
    prev_cust = prev.get("new_customers", 0)
    cust_change_str, _ = _calc_trend(cur_cust, prev_cust)
    rows.append(["New Customers", str(cur_cust), str(prev_cust), cust_change_str])

    # Churn rate
    cur_churn = cur.get("churn_rate", 0)
    prev_churn = prev.get("churn_rate", 0)
    churn_change_str, _ = _calc_trend(cur_churn, prev_churn)
    rows.append(["Churn Rate (%)", f"{cur_churn:.2f}%", f"{prev_churn:.2f}%", churn_change_str])

    table = Table(rows, colWidths=[150, 120, 120, 100])
    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ])
    table.setStyle(style)
    return table
