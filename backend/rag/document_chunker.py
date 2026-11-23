def create_chunks(pages, chunk_size=1000, overlap=150):
    chunks = []
    chunk_index = 0

    for page in pages:
        page_number = page["page_number"]
        text = page["text"].strip()

        if not text:
            continue

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "chunk_index": chunk_index,
                    "page_number": page_number,
                    "chunk_text": chunk_text
                })

                chunk_index += 1

            if end >= len(text):
                break

            start = end - overlap

    return chunks