#!/bin/sh
# wait-for-clickhouse.sh

set -e

host="$1"
shift
cmd="$@"

echo "⏳ Waiting for ClickHouse at $host:9000..."

until nc -z "$host" 9000; do
  >&2 echo "ClickHouse is unavailable - sleeping"
  sleep 2
done

>&2 echo "✅ ClickHouse is up - executing command"
exec $cmd
