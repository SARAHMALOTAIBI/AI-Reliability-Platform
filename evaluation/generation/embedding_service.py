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


def pairwise_semantic_similarity(
    texts_a: list[str],
    texts_b: list[str],
) -> np.ndarray:
    """
    Return a semantic similarity matrix.

    Shape:
        len(texts_a) x len(texts_b)
    """

    clean_a = [
        text.strip()
        for text in texts_a
        if text and text.strip()
    ]

    clean_b = [
        text.strip()
        for text in texts_b
        if text and text.strip()
    ]

    if not clean_a or not clean_b:
        return np.zeros(
            (
                len(clean_a),
                len(clean_b),
            ),
            dtype=float,
        )

    embeddings = get_embedding_model().encode(
        clean_a + clean_b,
        normalize_embeddings=True,
    )

    a_embeddings = embeddings[
        : len(clean_a)
    ]

    b_embeddings = embeddings[
        len(clean_a) :
    ]

    matrix = np.matmul(
        a_embeddings,
        b_embeddings.T,
    )

    return np.clip(
        matrix,
        0.0,
        1.0,
    )


def semantic_similarity(
    text_a: str,
    text_b: str,
) -> float:
    """
    Calculate semantic similarity between two texts.

    Returns a score between 0 and 1.
    """

    clean_a = text_a.strip()
    clean_b = text_b.strip()

    if not clean_a or not clean_b:
        return 0.0

    matrix = pairwise_semantic_similarity(
        [clean_a],
        [clean_b],
    )

    score = float(
        matrix[0][0]
    )

    return round(
        max(
            0.0,
            min(1.0, score),
        ),
        4,
    )
