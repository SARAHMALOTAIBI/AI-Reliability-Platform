"""
Verification Agent
===================
Checks whether a RAG-generated answer is actually supported by the
company's real indexed documents (not just the context the RAG
application claimed to retrieve).
"""

from dataclasses import dataclass

from knowledge_base.vector_store import query_similar_chunks


@dataclass(frozen=True)
class VerificationResult:
    is_supported: bool
    best_match_text: str
    best_match_source: str
    similarity_distance: float
    explanation: str


# Below this distance, we consider the match "relevant enough"
RELEVANCE_THRESHOLD = 0.8


def verify_answer(
    collection_name: str,
    question: str,
    top_k: int = 3,
) -> VerificationResult:
    """
    Searches the real knowledge base for the question and reports
    whether relevant supporting information actually exists.

    This does NOT check the RAG app's own retrieved context — it
    independently verifies against the company's real documents.

    Args:
        collection_name: The project's document collection to search.
        question: The original user question.
        top_k: How many candidate matches to consider.

    Returns:
        A VerificationResult describing whether supporting evidence
        was found in the real knowledge base.
    """
    matches = query_similar_chunks(
        collection_name=collection_name,
        query=question,
        top_k=top_k,
    )

    if not matches:
        return VerificationResult(
            is_supported=False,
            best_match_text="",
            best_match_source="",
            similarity_distance=1.0,
            explanation=(
                "No documents found in the knowledge base for this "
                "project. The knowledge base may be empty or not yet "
                "indexed."
            ),
        )

    best_match = matches[0]
    is_supported = best_match["distance"] <= RELEVANCE_THRESHOLD

    if is_supported:
        explanation = (
            f"Found supporting information in '{best_match['source']}' "
            f"with similarity distance {best_match['distance']:.4f}."
        )
    else:
        explanation = (
            f"No sufficiently relevant information found in the "
            f"knowledge base (closest match distance: "
            f"{best_match['distance']:.4f}, threshold: "
            f"{RELEVANCE_THRESHOLD}). This suggests the knowledge base "
            f"may be missing information needed to answer this question."
        )

    return VerificationResult(
        is_supported=is_supported,
        best_match_text=best_match["text"],
        best_match_source=best_match["source"],
        similarity_distance=best_match["distance"],
        explanation=explanation,
    )