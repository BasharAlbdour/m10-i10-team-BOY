# Team Roster — Module 10 Integration

This file is the team roster artifact for the Module 10 four-service
Docker Compose Integration.

> **No personal names** in this file. The team grading and TA
> cross-reference use `git log --author=<email>` for attribution.

---

## Team Identity

- **Team name:** team-BOY
- **Team Slack channel:** #m10-team-BOY
- **Team-formation date:** 2026-06-24
- **Designated team submitter:** Infra-Integration lead (BA)

---

## Team Roster

| Role | Team Member identifier | Assigned by | Branch | Internal-PR reviewer | Primary files owned |
|---|---|---|---|---|---|
| Backend lead | OH | Instructional team | `backend/api-endpoints` | Frontend lead (YM) | `api/main.py`, `api/models.py`, `api/rag.py`, `api/deps.py`, `api/Dockerfile` |
| Frontend lead | YM | Instructional team | `frontend/nextjs-pages` | Backend lead (OH) | `web/pages/{extract,kg,rag}.tsx`, `web/lib/types.ts`, `web/Dockerfile`, `tests/frontend/playwright/*` |
| Infra-Integration lead | BA | Instructional team | `infra/docker-compose` | Backend lead (OH) | `docker-compose.yml`, `scripts/seed_neo4j.sh`, `scripts/seed_weaviate.sh`, `scripts/healthcheck_stack.sh`, `.env.example`, `README.md`, `tests/integration/test_stack_e2e.py` |

**Fallback compositions for non-3-Team-Member teams:**

- **2 Team Members:** Frontend and Infra-Integration roles merge. The merged Team Member owns all `web/`, `docker-compose.yml`, and `seed_*.sh` files.
- **4 Team Members:** Infra-Integration splits into "Compose + healthchecks" and "Seed + runbook".

---

## Per-Role File Checklist (used for TA grading cross-reference)

The TA cross-references this checklist against `git log --author=<email>` on the team fork during per-role grading. Check the box when the Team Member confirms they authored the file.

### Backend lead (OH)

- [x] `api/main.py` — path operations, `lifespan`, CORS middleware
- [ ] `api/models.py` — Pydantic shapes
- [x] `api/rag.py` — RAG composer with grounding contract
- [ ] `api/deps.py` — `Depends()` functions
- [ ] `api/Dockerfile` — single-stage Python

### Frontend lead (YM)

- [ ] `web/pages/extract.tsx` 
- [ ] `web/pages/kg.tsx`
- [ ] `web/pages/rag.tsx`
- [ ] `web/lib/types.ts` — three TypeScript interfaces mirroring Pydantic
- [ ] `web/Dockerfile` — multi-stage Node
- [x] `tests/frontend/playwright/*.spec.ts` — one per page

### Infra-Integration lead (BA)

- [x] `docker-compose.yml` — four services, healthchecks, `depends_on` chain, named volumes
- [x] `scripts/seed_neo4j.sh`
- [x] `scripts/seed_weaviate.sh`
- [x] `scripts/healthcheck_stack.sh`
- [x] `.env.example` (no real credentials)
- [x] `README.md` runbook
- [x] `tests/integration/test_stack_e2e.py`

---

## Escalation Checklist (apply in order)

When a disagreement about scope, role boundaries, or contract changes arises:

1. **Inline comment on the internal PR.** State the disagreement specifically and link the contract artifact (Pydantic shape, TypeScript interface, Compose service entry).
2. **Team Slack channel with TA tagged.** Tag the TA who covers the team. Allow up to 4 working hours for response.
3. **Support Instructor.** If the TA decision is contested or the TA is unavailable, escalate to the Support Instructor via the cohort Slack channel.
4. **Lead Instructor.** Only if a role-rebalancing decision is needed or the disagreement is not resolved by the Support Instructor.

Document the escalation path taken in the team submission PR description.

---

## Contract-Change Protocol

- **Backend lead (OH)** announces any Pydantic shape change on the team Slack channel **before** the change lands.
- **Frontend lead (YM)** requests new backend fields via an internal-PR comment on the Backend lead's branch — does not assume.
- **Infra-Integration lead (BA)** announces any `.env` or DNS-affecting change before the change lands.

The protocol is enforced by the internal-PR review — the reviewer rejects PRs where the contract change was not announced.

---

## Submission

When all three role branches merge to the team fork's `main` and `docker compose up -d` smoke passes locally for each Team Member:

1. BA (team submitter) opens the PR from `https://github.com/BasharAlbdour/m10-i10-team-BOY` to upstream.
2. Each Team Member separately submits the participation-confirmation TalentLMS unit naming their assigned role and the files they authored.

The two-tier grading model (team tier 60 pts + per-role tier 40 pts) is described in the team-facing Integration Spec at <https://LevelUp-Applied-AI.github.io/aispire-14005-pages/modules/module-10/4ba363ed>.
