# app/api/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

api_bp = Blueprint("api", __name__)

# Mock KPI dataset
MOCK_KPIS = [
    {"region": "NA", "total_sales": 5000000},
    {"region": "EU", "total_sales": 3200000},
    {"region": "APAC", "total_sales": 2100000},
]

@api_bp.route("/kpi-summary", methods=["GET"])
# @jwt_required()
def get_kpi_summary():
    # Get filters from query parameters
    date_range = request.args.get("dateRange", "last_30_days")
    region = request.args.get("region", "all")

    # For now, just mock filter logic
    data = MOCK_KPIS
    if region != "all":
        data = [kpi for kpi in MOCK_KPIS if kpi["region"] == region]

    # Optionally mock different results per date range
    if date_range == "last_7_days":
        data = [{**kpi, "total_sales": int(kpi["total_sales"] * 0.2)} for kpi in data]
    elif date_range == "last_90_days":
        data = [{**kpi, "total_sales": int(kpi["total_sales"] * 1.5)} for kpi in data]
    elif date_range == "year_to_date":
        data = [{**kpi, "total_sales": int(kpi["total_sales"] * 4)} for kpi in data]

    return jsonify(data)
