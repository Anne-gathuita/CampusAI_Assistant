
from rag.source_retriever import (
    get_chunk_source,
    search_chunks_with_sources
)

from rag.vector_store import store_chunks


# Get our temporary test document from MySQL
source = get_chunk_source(1, 0)

if source:

    # Store the same document chunk in ChromaDB
    store_chunks(
        [{
            "chunk_index": 0,
            "page_number": source["page_number"],
            "chunk_text": source["chunk_text"]
        }],
        document_id=1
    )

    # Search ChromaDB and retrieve the original source
    results = search_chunks_with_sources(
        "temporary sample text for testing PDF extraction and database storage"
    )

    print("\nSEARCH RESULTS WITH ORIGINAL SOURCES:")

    for result in results:
        print("\nText:", result["chunk_text"])
        print("Document:", result["source"]["title"])
        print("Version:", result["source"]["version"])
        print("Page:", result["source"]["page_number"])

else:
    print("Test document not found in MySQL.")
