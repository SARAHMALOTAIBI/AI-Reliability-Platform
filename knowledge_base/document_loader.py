"""Document loading helpers."""

import pymupdf


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from all PDF pages."""
    with pymupdf.open(file_path) as document:
        return "\n".join(page.get_text() for page in document)
