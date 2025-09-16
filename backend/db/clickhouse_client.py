import clickhouse_connect
from config import Config

client = clickhouse_connect.get_client(
    host="clickhouse",
    port=8123,        # ✅ use HTTP port
    username="default",
    password="mypassword",
    database="analytics"
    # host=Config.CLICKHOUSE_HOST,
    # port=Config.CLICKHOUSE_PORT,
    # username=Config.CLICKHOUSE_USER,
    # password=Config.CLICKHOUSE_PASSWORD,
    # database=Config.CLICKHOUSE_DATABASE
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
