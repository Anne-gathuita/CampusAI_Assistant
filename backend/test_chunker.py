from rag.document_chunker import create_chunks

sample_pages = [
    {
        "page_number": 1,
        "text": "This is a sample university handbook. " * 100
    },
    {
        "page_number": 2,
        "text": "This page contains examination regulations. " * 100
    }
]

chunks = create_chunks(sample_pages)

print("Total chunks:", len(chunks))

for chunk in chunks:
    print("\nChunk index:", chunk["chunk_index"])
    print("Page number:", chunk["page_number"])
    print("Text:", chunk["chunk_text"][:100])