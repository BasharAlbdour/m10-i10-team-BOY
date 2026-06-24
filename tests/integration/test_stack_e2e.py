"""End-to-end smoke harness — Infra-Integration lead authors.

Verifies the four-service stack is up and the demo /rag/answer endpoint
returns HTTP 200 with citations against the seeded fixture.

The autograder does not run this file; it is intended for local
demo-prep and TA walkthroughs.

Run from the repo root with the stack already up and seeded:

    pytest tests/integration/test_stack_e2e.py -v
"""

import requests

API_BASE = "http://localhost:8000"
DEMO_QUESTION = "How do I prep ginger for stir-fry?"


def test_healthz():
    """API is reachable and reports healthy."""
    response = requests.get(f"{API_BASE}/healthz", timeout=5)

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_readyz():
    """API reports Neo4j and Weaviate are ready."""
    response = requests.get(f"{API_BASE}/readyz", timeout=5)

    assert response.status_code == 200

    data = response.json()

    assert data["neo4j"] == "ok"
    assert data["weaviate"] == "ok"


def test_rag_answer_returns_200_with_citations():
    """Demo question returns citations and confidence."""
    response = requests.post(
        f"{API_BASE}/rag/answer",
        json={"question": DEMO_QUESTION},
        timeout=60,
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "citations" in data
    assert "confidence" in data

    assert isinstance(data["answer"], str)
    assert isinstance(data["citations"], list)
    assert isinstance(data["confidence"], (int, float))

    assert len(data["citations"]) > 0
    assert data["confidence"] > 0


def test_rag_answer_citation_shape():
    """Each citation contains chunk_id and score."""
    response = requests.post(
        f"{API_BASE}/rag/answer",
        json={"question": DEMO_QUESTION},
        timeout=60,
    )

    assert response.status_code == 200

    citations = response.json()["citations"]

    assert len(citations) > 0

    for citation in citations:
        assert "chunk_id" in citation
        assert "score" in citation
        assert citation["score"] > 0


def test_rag_answer_idempotent():
    """Repeated calls return the same citations."""

    payload = {"question": DEMO_QUESTION}

    response_1 = requests.post(
        f"{API_BASE}/rag/answer",
        json=payload,
        timeout=60,
    )

    response_2 = requests.post(
        f"{API_BASE}/rag/answer",
        json=payload,
        timeout=60,
    )

    assert response_1.status_code == 200
    assert response_2.status_code == 200

    assert response_1.json()["citations"] == response_2.json()["citations"]