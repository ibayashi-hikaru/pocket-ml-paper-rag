"""Tests for PDF extraction."""

import pytest
from pathlib import Path

from app.pdf_extraction import extract_text_from_pdf, _clean_text


def test_clean_text():
    """Test text cleaning function."""
    dirty_text = "  This   is   a   test  \n\n\n  with   multiple   spaces  "
    cleaned = _clean_text(dirty_text)
    assert "  " not in cleaned
    assert cleaned.count("\n") <= len(cleaned.split("\n")) - 1


def test_extract_text_from_pdf_nonexistent():
    """Test extraction from non-existent file."""
    with pytest.raises((ValueError, FileNotFoundError)):
        extract_text_from_pdf(Path("nonexistent.pdf"))


# Note: To test with actual PDFs, you would need sample PDF files
# def test_extract_text_from_pdf_real():
#     """Test extraction from real PDF."""
#     pdf_path = Path("tests/sample.pdf")
#     if pdf_path.exists():
#         text = extract_text_from_pdf(pdf_path)
#         assert len(text) > 0
#         assert isinstance(text, str)

