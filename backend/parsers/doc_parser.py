import io
import os
import re
from pypdf import PdfReader
from docx import Document


def clean_text(text: str) -> str:
    """
    Cleans up excessive whitespace, normalizes newlines, and strips
    unprintable control characters while preserving document structure.
    """
    if not text:
        return ""

    # Remove unprintable characters (keep newlines and tabs)
    text = "".join(char for char in text if char.isprintable() or char in "\n\r\t")

    # Normalize carriage returns
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Collapse 3 or more consecutive newlines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Trim redundant spaces and tabs within lines
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """
    Detects file extension (.pdf, .docx, .txt, .md) and extracts clean,
    normalized plain text from raw file bytes.
    """
    ext = os.path.splitext(filename)[1].lower()

    if not file_bytes:
        raise ValueError(f"File '{filename}' is empty.")

    raw_text = ""

    # 1. PDF extraction using pypdf
    if ext == ".pdf":
        pdf_stream = io.BytesIO(file_bytes)
        reader = PdfReader(pdf_stream)
        pages_text = []
        for page in reader.pages:
            content = page.extract_text()
            if content:
                pages_text.append(content.strip())
        raw_text = "\n\n".join(pages_text)

    # 2. Word (.docx) extraction using python-docx
    elif ext == ".docx":
        docx_stream = io.BytesIO(file_bytes)
        doc = Document(docx_stream)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

        # Also collect text from tables if present
        for table in doc.tables:
            for row in table.rows:
                row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_text:
                    paragraphs.append(" | ".join(row_text))

        raw_text = "\n\n".join(paragraphs)

    # 3. Plain Text and Markdown
    elif ext in [".txt", ".md"]:
        try:
            raw_text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raw_text = file_bytes.decode("latin-1", errors="ignore")

    else:
        raise ValueError(
            f"Unsupported file format: '{ext}'. Supported formats are: .pdf, .docx, .txt, .md"
        )

    return clean_text(raw_text)
