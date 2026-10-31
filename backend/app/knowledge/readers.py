"""
Liest den reinen Text aus hochgeladenen Dateien.
Unterstuetzt: txt, md, csv, json, docx, pdf.
"""
import io
from pathlib import Path

TEXT_TYPES = {".txt", ".md", ".csv", ".json"}
SUPPORTED = TEXT_TYPES | {".docx", ".pdf"}


class ReadError(Exception):
    pass


def read_text(filename: str, data: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED:
        raise ReadError(
            f"Dateityp '{suffix or 'ohne Endung'}' wird nicht unterstuetzt. "
            f"Erlaubt: {', '.join(sorted(SUPPORTED))}."
        )
    if suffix in TEXT_TYPES:
        text = data.decode("utf-8", errors="replace")
    elif suffix == ".docx":
        text = _read_docx(data)
    else:
        text = _read_pdf(data)
    text = text.strip()
    if not text:
        raise ReadError("In der Datei wurde kein Text gefunden (bei PDFs: evtl. nur eingescannte Bilder).")
    return text


def _read_docx(data: bytes) -> str:
    from docx import Document  # erst bei Bedarf laden

    doc = Document(io.BytesIO(data))
    parts = [p.text for p in doc.paragraphs if p.text.strip()]
    for table in doc.tables:
        for row in table.rows:
            parts.append(" | ".join(c.text.strip() for c in row.cells))
    return "\n\n".join(parts)


def _read_pdf(data: bytes) -> str:
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(data))
    return "\n\n".join((page.extract_text() or "") for page in reader.pages)
