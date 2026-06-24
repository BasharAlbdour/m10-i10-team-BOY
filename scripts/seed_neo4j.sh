#!/usr/bin/env bash
# Seed the running Neo4j container with the recipe fixture.
# Idempotent — seed.cypher uses MERGE and CREATE CONSTRAINT IF NOT EXISTS.
# Run from the repo root (the directory containing docker-compose.yml).

set -euo pipefail

# Auto-load .env if present
if [[ -f .env ]]; then
  set -a && source .env && set +a
fi

NEO4J_USER="${NEO4J_USER:-neo4j}"
NEO4J_PASSWORD="${NEO4J_PASSWORD:?NEO4J_PASSWORD is not set. Copy .env.example to .env and fill in the value.}"

echo "Seeding Neo4j..."
docker compose exec -T neo4j cypher-shell \
  -u "$NEO4J_USER" \
  -p "$NEO4J_PASSWORD" \
  < api/seed.cypher

echo "Neo4j seed complete."
