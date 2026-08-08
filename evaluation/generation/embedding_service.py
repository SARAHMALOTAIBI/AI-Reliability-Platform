from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """
    Load the embedding model once and reuse it.
    """
    return SentenceTransformer(MODEL_NAME)


def semantic_similarity(text_a: str, text_b: str) -> float:
    """
    Calculate semantic similarity between two texts.

    Returns a score between 0 and 1.
    """
    clean_text_a = text_a.strip()
    clean_text_b = text_b.strip()

    if not clean_text_a or not clean_text_b:
        return 0.0

    embeddings = get_embedding_model().encode(
        [clean_text_a, clean_text_b],
        normalize_embeddings=True,
    )

    score = float(
        np.dot(
            embeddings[0],
            embeddings[1],
        )
    )

    normalized_score = max(
        0.0,
        min(1.0, score),
    )

    return round(normalized_score, 4)
