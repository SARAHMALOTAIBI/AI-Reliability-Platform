"""
Indexing Service
=================
Orchestrates the full pipeline: extract text from an uploaded file,
split it into chunks, and store it in the vector database.
"""

import os

from knowledge_base.document_loader import extract_text_from_pdf
from knowledge_base.chunker import chunk_text
from knowledge_base.vector_store import add_chunks


def index_document(
    file_path: str,
    collection_name: str,
    source_name: str,
) -> dict:
    """
    Extracts, chunks, and stores a document in the vector database.

    Args:
        file_path: Path to the file on disk (already saved).
        collection_name: Project/collection to store the chunks under.
        source_name: Display name for the source (e.g. original filename).

    Returns:
        A dict summarizing the indexing result.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    text = extract_text_from_pdf(file_path)

    if not text.strip():
        return {
            "success": False,
            "chunks_indexed": 0,
            "message": "No text could be extracted from this file.",
        }

    chunks = chunk_text(text)

    add_chunks(
        collection_name=collection_name,
        chunks=chunks,
        source=source_name,
    )

    return {
        "success": True,
        "chunks_indexed": len(chunks),
        "message": f"Successfully indexed {len(chunks)} chunks from '{source_name}'.",
    }
