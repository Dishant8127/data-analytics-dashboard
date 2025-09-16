FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Install netcat for wait-for-clickhouse.sh
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY . .
RUN chmod +x wait-for-clickhouse.sh

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
