
import pymupdf
from datetime import date, datetime
from pathlib import Path

from rag.document_loader import load_document
from database import get_connection


# 1. Create a temporary sample PDF
pdf_path = Path("loader_test.pdf")

pdf = pymupdf.open()
page = pdf.new_page()

page.insert_text(
    (72, 72),
    "CampusAI Document Loader Test\n"
    "This is temporary sample text for testing PDF extraction, "
    "chunking, and database storage."
)

pdf.save(str(pdf_path))
pdf.close()


# 2. Load the sample PDF into MySQL
try:
    result = load_document(
        pdf_path=pdf_path,
        title="TEMPORARY CAMPUSAI LOADER TEST "
              + datetime.now().strftime("%Y%m%d_%H%M%S"),
        document_type="test",
        version="1.0",
        effective_date=date.today(),
        approval_status="pending"
    )

    print("\nDOCUMENT LOADED SUCCESSFULLY!")
    print("Document ID:", result["document_id"])
    print("Pages:", result["pages"])
    print("Chunks:", result["chunks"])

    # 3. Verify that the chunks were saved
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT chunk_index, page_number, chunk_text
        FROM document_chunks
        WHERE document_id = %s
        """,
        (result["document_id"],)
    )

    print("\nSAVED CHUNKS:")
    for row in cursor.fetchall():
        print(row)

    cursor.close()
    connection.close()

except Exception as error:
    print("\nDOCUMENT LOADING FAILED:")
    print(error)
