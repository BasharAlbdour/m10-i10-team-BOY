#!/usr/bin/env bash
# Poll docker compose ps until all four services report healthy
# or until the 90s budget expires.
# Run from the repo root.

set -euo pipefail

# Auto-load .env if present
if [[ -f .env ]]; then
  set -a && source .env && set +a
fi

SERVICES=("neo4j" "weaviate" "api" "web")
MAX_ITERATIONS=45
SLEEP=2

echo "Waiting for all services to become healthy (budget: $((MAX_ITERATIONS * SLEEP))s)..."

for i in $(seq 1 $MAX_ITERATIONS); do
  all_healthy=true

  for svc in "${SERVICES[@]}"; do
    status=$(docker compose ps --format json "$svc" 2>/dev/null \
      | python3 -c "import sys,json; data=sys.stdin.read().strip(); rows=data.splitlines(); obj=json.loads(rows[0]) if rows else {}; print(obj.get('Health',''))" 2>/dev/null || echo "")

    if [[ "$status" != "healthy" ]]; then
      all_healthy=false
      break
    fi
  done

  if $all_healthy; then
    echo "All services healthy."
    exit 0
  fi

  echo "  Attempt $i/$MAX_ITERATIONS — not all healthy yet, retrying in ${SLEEP}s..."
  sleep $SLEEP
done

echo "ERROR: Timed out waiting for services to become healthy."
docker compose ps
exit 1
