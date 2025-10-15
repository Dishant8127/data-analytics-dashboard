

# import clickhouse_connect
# from config import Config
# import os

# client = clickhouse_connect.get_client(
#     # host="clickhouse",
#     # port=8123,        # ✅ use HTTP port
#     # username="default",
#     # password="mypassword",
#     # database="analytics"
#     host=os.getenv("CLICKHOUSE_HOST", "localhost"),   # must be localhost
#     port=int(os.getenv("CLICKHOUSE_PORT", "8123")),
#     username=os.getenv("CLICKHOUSE_USER", "default"),
#     password=os.getenv("CLICKHOUSE_PASSWORD", ""),
#     database=os.getenv("CLICKHOUSE_DATABASE", "analytics"),

# )

# def fetch_region_kpis(region: str, date_range: str = "last_7_days"):
#     # Build dynamic query (simplified example)
#     query = f"""
#         SELECT region,
#                SUM(sales) AS total_sales,
#                COUNT(DISTINCT customer_id) AS new_customers,
#                AVG(churn_rate) AS churn_rate
#         FROM kpi_data
#         WHERE region = %(region)s
#           AND event_date >= today() - INTERVAL 7 DAY
#         GROUP BY region
#     """

#     result = client.query(query, parameters={"region": region})
#     rows = result.result_rows

#     # Convert to dict
#     kpis = []
#     for row in rows:
#         kpis.append({
#             "region": row[0],
#             "total_sales": row[1],
#             "new_customers": row[2],
#             "churn_rate": row[3]
#         })
#     return kpis


# def fetch_region_product_kpis(region: str, date_range: str = "last_7_days"):
#     query = f"""
#         SELECT 
#             product_category,
#             SUM(sales) AS total_sales,
#             COUNT(DISTINCT customer_id) AS new_customers,
#             AVG(churn_rate) AS churn_rate
#         FROM kpi_data
#         WHERE region = %(region)s
#           AND event_date >= today() - INTERVAL 7 DAY
#         GROUP BY product_category
#         ORDER BY total_sales DESC
#         LIMIT 10
#     """
#     result = client.query(query, parameters={"region": region})
#     rows = result.result_rows

#     kpis = []
#     for row in rows:
#         kpis.append({
#             "product_category": row[0],
#             "total_sales": row[1],
#             "new_customers": row[2],
#             "churn_rate": row[3]
#         })
#     return kpis




import clickhouse_connect
from config import Config
import os

client = clickhouse_connect.get_client(
    # host="clickhouse",
    # port=8123,        # ✅ use HTTP port
    # username="default",
    # password="mypassword",
    # database="analytics"
    host=os.getenv("CLICKHOUSE_HOST", "localhost"),
    port=int(os.getenv("CLICKHOUSE_PORT", 8123)),
    username=os.getenv("CLICKHOUSE_USER", "default"),
    password=os.getenv("CLICKHOUSE_PASSWORD", ""),
    database=os.getenv("CLICKHOUSE_DATABASE", "analytics"),
)




def fetch_region_kpis(region: str, date_range: str = "last_7_days"):
    # Build dynamic query (simplified example)
    query = f"""
        SELECT region,
               SUM(sales) AS total_sales,
               COUNT(DISTINCT customer_id) AS new_customers,
               AVG(churn_rate) AS churn_rate
        FROM kpi_data
        WHERE region = %(region)s
          AND event_date >= today() - INTERVAL 7 DAY
        GROUP BY region
    """

    result = client.query(query, parameters={"region": region})
    rows = result.result_rows

    # Convert to dict
    kpis = []
    for row in rows:
        kpis.append({
            "region": row[0],
            "total_sales": row[1],
            "new_customers": row[2],
            "churn_rate": row[3]
        })
    return kpis


def fetch_region_product_kpis(region: str, date_range: str = "last_7_days"):
    query = f"""
        SELECT 
            product_category,
            SUM(sales) AS total_sales,
            COUNT(DISTINCT customer_id) AS new_customers,
            AVG(churn_rate) AS churn_rate
        FROM kpi_data
        WHERE region = %(region)s
          AND event_date >= today() - INTERVAL 7 DAY
        GROUP BY product_category
        ORDER BY total_sales DESC
        LIMIT 10
    """
    result = client.query(query, parameters={"region": region})
    rows = result.result_rows

    kpis = []
    for row in rows:
        kpis.append({
            "product_category": row[0],
            "total_sales": row[1],
            "new_customers": row[2],
            "churn_rate": row[3]
        })
    return kpis


def fetch_region_kpi_trends(region: str, period_days: int = 7):
    """
    Fetch current and previous period KPIs for trend calculation.
    """
    query = f"""
        SELECT
            'current' as period,
            SUM(sales) AS total_sales,
            COUNT(DISTINCT customer_id) AS new_customers,
            AVG(churn_rate) AS churn_rate
        FROM kpi_data
        WHERE region = %(region)s
          AND event_date >= today() - INTERVAL {period_days} DAY

        UNION ALL

        SELECT
            'previous' as period,
            SUM(sales) AS total_sales,
            COUNT(DISTINCT customer_id) AS new_customers,
            AVG(churn_rate) AS churn_rate
        FROM kpi_data
        WHERE region = %(region)s
          AND event_date >= today() - INTERVAL {period_days*2} DAY
          AND event_date < today() - INTERVAL {period_days} DAY
    """

    result = client.query(query, parameters={"region": region})
    rows = {
        row[0]: {
            "total_sales": row[1],
            "new_customers": row[2],
            "churn_rate": row[3]
        }
        for row in result.result_rows
    }

    return rows.get("current", {}), rows.get("previous", {})
