from flask import Blueprint, request, jsonify, Response
import csv
import io

api_bp = Blueprint("api", __name__)

# -------------------------
# Mock KPI dataset
# -------------------------
MOCK_KPIS = [
    {"region": "NA", "total_sales": 5000000},
    {"region": "EU", "total_sales": 3200000},
    {"region": "APAC", "total_sales": 2100000},
]

# -------------------------
# KPI Summary Endpoint
# -------------------------
@api_bp.route("/kpi-summary", methods=["GET"])
def get_kpi_summary():
    # Get filters from query parameters
    date_range = request.args.get("dateRange", "last_30_days")
    region = request.args.get("region", "all")

    # Apply region filter
    data = MOCK_KPIS
    if region != "all":
        data = [kpi for kpi in MOCK_KPIS if kpi["region"] == region]

    # Apply date range adjustments (mock logic)
    if date_range == "last_7_days":
        data = [{**kpi, "total_sales": int(kpi["total_sales"] * 0.2)} for kpi in data]
    elif date_range == "last_90_days":
        data = [{**kpi, "total_sales": int(kpi["total_sales"] * 1.5)} for kpi in data]
    elif date_range == "year_to_date":
        data = [{**kpi, "total_sales": int(kpi["total_sales"] * 4)} for kpi in data]

    return jsonify(data)

# -------------------------
# CSV Export Endpoint
# -------------------------
@api_bp.route("/export-csv", methods=["GET"])
def export_csv():
    # Get filters from query parameters
    date_range = request.args.get("dateRange", "last_30_days")
    region = request.args.get("region", "all")

    # Apply region filter
    data = MOCK_KPIS
    if region != "all":
        data = [kpi for kpi in MOCK_KPIS if kpi["region"] == region]

    # Apply date range adjustments (mock logic)
    if date_range == "last_7_days":
        data = [{**kpi, "total_sales": int(kpi["total_sales"] * 0.2)} for kpi in data]
    elif date_range == "last_90_days":
        data = [{**kpi, "total_sales": int(kpi["total_sales"] * 1.5)} for kpi in data]
    elif date_range == "year_to_date":
        data = [{**kpi, "total_sales": int(kpi["total_sales"] * 4)} for kpi in data]

    # Generate CSV in memory
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["region", "total_sales"])
    writer.writeheader()
    writer.writerows(data)

    # Return CSV file
    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=kpi_export.csv"
    return response




