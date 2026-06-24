# Integration 10 — Dockerize the Four-Service Stack

Compose the Lab's FastAPI backend and Next.js frontend with **containerized Neo4j and Weaviate** into a one-command Dockerized stack delivered as a 3-Team-Member team.

> Read the full Integration guide on the cohort site:
>
> https://LevelUp-Applied-AI.github.io/aispire-14005-pages/modules/module-10/a0cae6a2
>
> Team-facing spec:
>
> https://LevelUp-Applied-AI.github.io/aispire-14005-pages/modules/module-10/4ba363ed

## Team Roles

See [TEAM.md](TEAM.md) for role assignments and the per-role file checklist.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the internal-PR review convention and the contract-change protocol.

---

## Starter Layout

```text
api/                      FastAPI backend (Backend lead extends)

web/                      Next.js frontend (Frontend lead extends)

docker-compose.yml        Four-service Compose stack

scripts/
  seed_neo4j.sh           Seeds Neo4j with recipe fixture
  seed_weaviate.sh        Seeds Weaviate with chunked-docs fixture
  healthcheck_stack.sh    Polls until all four services are healthy

.env.example              Placeholder credentials — copy to .env

TEAM.md                   Team roster and per-role file checklist

CONTRIBUTING.md           Branch convention and internal-PR protocol
```

---

## Runbook — End-to-End from Clone to Browser Demo

### 1. Clone and Configure

```bash
git clone https://github.com/BasharAlbdour/m10-i10-team-BOY.git
cd m10-i10-team-BOY

cp .env.example .env
```

Open `.env` and set a password:

```env
NEO4J_AUTH=neo4j/yourpassword
NEO4J_USER=neo4j
NEO4J_PASSWORD=yourpassword
WEB_ORIGIN=http://localhost:3000
```

`NEO4J_AUTH` and `NEO4J_PASSWORD` must use the same password value.

Never commit `.env` — it is gitignored.

---

### 2. Build and Start the Stack

```bash
docker compose up -d --build
docker compose ps
```

The first build downloads model weights and container images. Expect several minutes on a fresh machine depending on network speed and Docker cache state.

---

### 3. Verify All Services Are Healthy

```bash
bash scripts/healthcheck_stack.sh
```

Expected output:

```text
All services healthy.
```

You can also verify manually:

```bash
docker compose ps
```

All four services must report healthy:

```text
neo4j
weaviate
api
web
```

---

### 4. Seed the Data Tiers

```bash
bash scripts/seed_neo4j.sh
bash scripts/seed_weaviate.sh
```

Both scripts are idempotent — re-running them does not duplicate data.

Expected results:

```text
Neo4j seed complete.
Weaviate seed complete.
```

---

### 5. Verify the API

```bash
curl http://localhost:8000/healthz
```

Expected:

```json
{"status":"ok"}
```

Verify readiness:

```bash
curl http://localhost:8000/readyz
```

Expected:

```json
{
  "neo4j": "ok",
  "weaviate": "ok"
}
```

---

### 6. Run the Demo RAG Query

```bash
curl -s -X POST http://localhost:8000/rag/answer \
  -H "Content-Type: application/json" \
  -d '{"question":"How do I prep ginger for stir-fry?"}'
```

Expected:

* HTTP 200 response
* Non-empty `citations` array
* `confidence > 0`

Example:

```json
{
  "answer": "...",
  "citations": [
    {
      "chunk_id": 4,
      "score": 0.78
    }
  ],
  "confidence": 0.78
}
```

---

### 7. Open the Web UI

Open:

```text
http://localhost:3000/rag
```

Use the seeded demo question:

```text
Find Sichuan recipes that use ginger
```

Verify that a cited answer is displayed.

> Do not start the FastAPI or Next.js applications manually.
> `docker compose up -d --build` starts all four services automatically.
---

### 8. Tear Down the Stack

```bash
docker compose down -v
```

The `-v` flag removes named volumes so the next run starts from a clean state.

If you bring the stack up again, re-run the seed scripts.

---

## Submission

### Team Submission

The designated team submitter:

* Opens the team submission PR (if required by the cohort workflow), or
* Pastes the team fork's `main` branch URL into TalentLMS → Module 10 → Integration Task.

### Per-Team-Member Participation Confirmation

Each Team Member separately submits:

* Their assigned role
* The files they authored
* Participation confirmation

---

## License

This repository is provided for educational use only.

See [LICENSE](LICENSE) for terms.

You may clone and modify this repository for personal learning and practice, and reference code you wrote here in your professional portfolio.

Redistribution outside this course is not permitted.
