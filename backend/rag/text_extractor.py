import pymupdf
from pathlib import Path


def extract_pdf_text(pdf_path):
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    extracted_pages = []

    with pymupdf.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")

            extracted_pages.append({
                "page_number": page_number,
                "text": text.strip()
            })

    return extracted_pages