"""PDF text extraction module."""

from pathlib import Path
from typing import Optional

from pdfminer.high_level import extract_text as pdfminer_extract
from pdfminer.layout import LAParams


def extract_text_from_pdf(pdf_path: Path, max_chars: Optional[int] = None) -> str:
    """
    Extract text from a PDF file.

    Args:
        pdf_path: Path to the PDF file
        max_chars: Optional maximum number of characters to extract

    Returns:
        Extracted text as a string
    """
    try:
        # Use pdfminer.six for robust text extraction
        laparams = LAParams(
            line_margin=0.5,
            word_margin=0.1,
            char_margin=2.0,
            boxes_flow=0.5,
        )

        text = pdfminer_extract(str(pdf_path), laparams=laparams)

        # Clean and normalize text
        text = _clean_text(text)

        # Limit length if specified
        if max_chars and len(text) > max_chars:
            text = text[:max_chars]

        return text

    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")


def _clean_text(text: str) -> str:
    """
    Clean and normalize extracted text.

    Args:
        text: Raw extracted text

    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line:
            cleaned_lines.append(line)

    # Join with single newlines
    text = "\n".join(cleaned_lines)

    # Remove excessive spaces
    while "  " in text:
        text = text.replace("  ", " ")

    return text


def extract_title_from_pdf(pdf_path: Path) -> Optional[str]:
    """
    Attempt to extract title from the first page of PDF.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted title or None
    """
    try:
        text = extract_text_from_pdf(pdf_path, max_chars=2000)
        # First non-empty line is often the title
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        if lines:
            return lines[0]
        return None

    except Exception:
        return None

