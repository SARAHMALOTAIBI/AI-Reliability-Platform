"""Document indexing orchestration."""

from __future__ import annotations

import hashlib
import os

from knowledge_base.chunker import chunk_text
from knowledge_base.document_loader import extract_text_from_pdf
from knowledge_base.vector_store import add_chunks


def calculate_file_sha256(
    file_path: str,
) -> str:
    digest = hashlib.sha256()

    with open(file_path, "rb") as file_handle:
        for block in iter(
            lambda: file_handle.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def index_document(
    file_path: str,
    project_id: str,
    source_name: str,
    document_id: str,
) -> dict:
    """Extract, chunk, embed, and persist one PDF in Chroma."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    text = extract_text_from_pdf(
        file_path
    )

    if not text.strip():
        return {
            "success": False,
            "document_id": document_id,
            "chunks_indexed": 0,
            "message": (
                "No text could be extracted "
                "from this PDF."
            ),
        }

    chunks = chunk_text(text)

    add_chunks(
        project_id=project_id,
        chunks=chunks,
        source=source_name,
        document_id=document_id,
    )

    return {
        "success": True,
        "document_id": document_id,
        "chunks_indexed": len(chunks),
        "message": (
            f"Successfully indexed "
            f"{len(chunks)} chunks from "
            f"'{source_name}'."
        ),
    }
