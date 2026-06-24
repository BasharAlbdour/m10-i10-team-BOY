"""RAG composer — retrieve → assemble → generate → cite → grounding check.

Grounding contract: when `answer` is not the empty-retrieval sentinel,
`len(citations) > 0` is required. Every cited `chunk_id` corresponds to
a chunk in the top-`k` retrieved from Weaviate.

Generator called with `do_sample=False` for reproducibility.
"""
import re
from typing import Tuple

PROMPT_TEMPLATE = """\
You are answering a recipe question. Use ONLY the numbered sources below.
Cite each claim with the source number in square brackets, e.g. [1].
If the sources do not contain the answer, say: I cannot answer this from the available sources.

Sources:
{sources}

Question: {question}
Answer:"""

SENTINEL = "I cannot answer this from the available sources"
CITATION_PATTERN = re.compile(r"\[(\d+)\]")


def empty_rag_response() -> dict:
    return {"answer": SENTINEL, "citations": [], "confidence": 0.0}


def assemble_prompt(question: str, chunks: list[dict]) -> Tuple[str, dict[int, dict]]:
    """Number the retrieved chunks 1..k and substitute into the prompt template.

    Returns (prompt_str, {citation_index: chunk_dict}). Index starts at 1.
    """
    numbered: dict[int, dict] = {}
    lines = []
    for i, chunk in enumerate(chunks, start=1):
        numbered[i] = chunk
        lines.append(f"[{i}] {chunk['text']}")
    sources = "\n".join(lines)
    return PROMPT_TEMPLATE.format(sources=sources, question=question), numbered


def extract_citations(answer: str, numbered: dict[int, dict]) -> list[dict]:
    """Pull [N]-style markers from `answer` and resolve to retrieved chunks.

    Returns one {"chunk_id", "score"} dict per unique resolvable index.
    """
    cited: list[dict] = []
    seen: set[int] = set()
    for match in CITATION_PATTERN.finditer(answer):
        idx = int(match.group(1))
        if idx in numbered and idx not in seen:
            seen.add(idx)
            chunk = numbered[idx]
            cited.append({"chunk_id": chunk["chunk_id"], "score": chunk["score"]})
    return cited


def parse_retrieved_chunks(raw_query) -> list[dict] | None:
    """Normalize Weaviate's response; return None for invalid shapes."""
    if not isinstance(raw_query, dict):
        return None
    data = raw_query.get("data")
    if not isinstance(data, dict):
        return None
    get_block = data.get("Get")
    if not isinstance(get_block, dict):
        return None
    chunks = get_block.get("Chunk")
    if not isinstance(chunks, list):
        return None

    retrieved = []
    for chunk in chunks:
        if not isinstance(chunk, dict):
            return None
        additional = chunk.get("_additional")
        if not isinstance(additional, dict):
            return None
        distance = additional.get("distance")
        if "chunk_id" not in chunk or "text" not in chunk or distance is None:
            return None
        try:
            score = 1.0 - float(distance)
        except (TypeError, ValueError):
            return None
        retrieved.append(
            {
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "score": score,
            }
        )
    return retrieved


def compose_rag(question: str, embedder, weaviate_client, generator, k: int = 4) -> dict:
    """Run the four-stage RAG pipeline.

    Encodes the question via the externally-loaded sentence-transformers
    embedder and queries Weaviate with `with_near_vector`. The Weaviate
    class is `vectorizer=none`, so `with_near_text` would fail at
    runtime with `KeyError: 'data'`.

    Returns {"answer": str, "citations": list[dict], "confidence": float}.
    """
    vector = embedder.encode(question).tolist()
    raw_query = (
        weaviate_client.query.get("Chunk", ["chunk_id", "text"])
        .with_near_vector({"vector": vector})
        .with_limit(k)
        .with_additional(["distance"])
        .do()
    )
    retrieved = parse_retrieved_chunks(raw_query)
    if not retrieved:
        return empty_rag_response()

    prompt, numbered = assemble_prompt(question, retrieved)
    raw = generator(prompt, max_new_tokens=256, do_sample=False)[0]["generated_text"]
    citations = extract_citations(raw, numbered)
    if not citations:
        return empty_rag_response()

    confidence = sum(c["score"] for c in citations) / len(citations)
    confidence = max(0.0, min(1.0, confidence))
    return {"answer": raw, "citations": citations, "confidence": confidence}
