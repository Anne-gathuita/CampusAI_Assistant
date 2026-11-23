
from database import get_connection
from rag.vector_store import search_chunks


def get_chunk_source(document_id, chunk_index):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                d.title,
                d.document_type,
                d.version,
                d.effective_date,
                dc.section_heading,
                dc.paragraph_reference,
                dc.page_number,
                dc.chunk_text

            FROM document_chunks dc

            JOIN documents d
                ON dc.document_id = d.id

            WHERE dc.document_id = %s
            AND dc.chunk_index = %s
            """,
            (document_id, chunk_index)
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


def search_chunks_with_sources(question, limit=3):

    matches = search_chunks(question, limit)

    results = []

    for match in matches:

        metadata = match["metadata"]

        source = get_chunk_source(
            metadata["document_id"],
            metadata["chunk_index"]
        )

        if source:
            results.append({
                "chunk_text": match["chunk_text"],
                "source": source
            })

    return results
