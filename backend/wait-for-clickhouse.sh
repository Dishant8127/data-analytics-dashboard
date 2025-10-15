
#!/bin/sh
# wait-for-clickhouse.sh

set -e

host="clickhouse"
port="9000"

echo "Waiting for ClickHouse at ${host}:${port}..."

while ! nc -z $host $port; do
  sleep 1
done

echo "ClickHouse is up!"
exec "$@"