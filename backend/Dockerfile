FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Install netcat for wait-for-clickhouse.sh
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY . .
COPY wait-for-clickhouse.sh /app/wait-for-clickhouse.sh
RUN chmod +x /app/wait-for-clickhouse.sh

CMD ["/app/wait-for-clickhouse.sh", "gunicorn", "-b", "0.0.0.0:5000", "run:app"]
