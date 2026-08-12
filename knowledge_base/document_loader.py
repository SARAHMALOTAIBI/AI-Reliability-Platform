"""
Document Loader
================
Extracts raw text from uploaded documents (currently PDF only).
"""

import fitz  # PyMuPDF


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts and returns all text content from a PDF file.

    Args:
        file_path: Path to the PDF file on disk.

    Returns:
        The full extracted text, with pages joined by newlines.
    """
    doc = fitz.open(file_path)
    pages_text = [page.get_text() for page in doc]
    doc.close()
    return "\n".join(pages_text)
