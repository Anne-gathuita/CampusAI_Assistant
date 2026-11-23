import pymupdf
from rag.text_extractor import extract_pdf_text

# Create a temporary PDF for testing
pdf = pymupdf.open()
page = pdf.new_page()

page.insert_text(
    (72, 72),
    "CampusAI PDF Extraction Test\n"
    "This is a sample document for testing."
)

pdf.save("sample_test.pdf")
pdf.close()

# Extract text from the PDF
pages = extract_pdf_text("sample_test.pdf")

for page in pages:
    print("Page:", page["page_number"])
    print("Extracted text:")
    print(page["text"])