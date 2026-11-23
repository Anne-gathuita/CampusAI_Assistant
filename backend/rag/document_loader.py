import os
import sys
import logging
import pathlib
from rag.vector_store import store_chunks

from rag.text_extractor import extract_pdf_text
from rag.document_chunker import create_chunks
from database import get_connection


def load_document(
    pdf_path,
    title,
    document_type,
    version,
    effective_date,
    approval_status="pending"
):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        pages = extract_pdf_text(pdf_path)

        cursor.execute(
            """
            INSERT INTO documents
            (title, document_type, version, effective_date,
             approval_status, file_path)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                title,
                document_type,
                version,
                effective_date,
                approval_status,
                str(pdf_path)
            )
        )

        document_id = cursor.lastrowid
        chunks = create_chunks(pages)

        for chunk in chunks:
            cursor.execute(
                """
                INSERT INTO document_chunks
                (document_id, chunk_index, page_number, chunk_text)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    document_id,
                    chunk["chunk_index"],
                    chunk["page_number"],
                    chunk["chunk_text"]
                )
            )

        connection.commit()
        vectors_stored = store_chunks(chunks, document_id)
        return {
            "document_id": document_id,
            "pages": len(pages),
            "chunks": len(chunks),
            "vectors_stored": vectors_stored
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()