"""
Text Chunker
============
Splits long text into smaller overlapping chunks, suitable for
embedding and retrieval.
"""


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[str]:
    """
    Splits text into overlapping chunks of a fixed character size.

    Args:
        text: The full text to split.
        chunk_size: Maximum number of characters per chunk.
        chunk_overlap: Number of characters shared between consecutive
                        chunks, to preserve context across boundaries.

    Returns:
        A list of text chunks.
    """
    clean_text = text.strip()

    if not clean_text:
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    chunks = []
    start = 0
    text_length = len(clean_text)

    while start < text_length:
        end = start + chunk_size
        chunk = clean_text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks
