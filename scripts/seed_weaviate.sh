#!/usr/bin/env bash
# Seed the running Weaviate container with the chunked-docs fixture.
# Idempotent — the seeder skips chunk_ids already present.
# Run from the repo root (the directory containing docker-compose.yml).

set -euo pipefail

# Auto-load .env if present
if [[ -f .env ]]; then
  set -a && source .env && set +a
fi

echo "Seeding Weaviate (runs inside the api container)..."
docker compose exec -T api python api/seed_weaviate.py

echo "Weaviate seed complete."
