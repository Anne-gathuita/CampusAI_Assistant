
from pathlib import Path
from datetime import date

from rag.document_loader import load_document

pdf_path = Path("uploads/GENERAL INFORMATION TO NEW STUDENT reviewed on 5th July 2025.pdf")

result = load_document(
    pdf_path=pdf_path,
    title="Maseno University - General Information to New Students",
    document_type="Student Information Guide",
    version="Reviewed 5 July 2025",
    effective_date=None,
    approval_status="pending"
)

print("\nMASENO UNIVERSITY DOCUMENT LOADED!")
print("Document ID:", result["document_id"])
print("Pages:", result["pages"])
print("Chunks:", result["chunks"])
print("Vectors stored:", result["vectors_stored"])
