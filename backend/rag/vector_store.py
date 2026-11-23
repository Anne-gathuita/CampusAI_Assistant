
import chromadb
from pathlib import Path

from rag.embeddings import model


# Where ChromaDB saves its information
DB_PATH = Path(__file__).resolve().parents[1] / "vector_db"

# Connect to ChromaDB
client = chromadb.PersistentClient(path=str(DB_PATH))


# Connect ChromaDB to our existing AI model
class CampusEmbeddingFunction( chromadb.EmbeddingFunction ):

    def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:

        embeddings = model.encode(input)

        return embeddings.tolist()


# Create or open a collection
def get_collection(collection_name="campusai_chunks"):

    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=CampusEmbeddingFunction()
    )

    return collection


# Save document chunks
def store_chunks(chunks, document_id):

    collection = get_collection()

    for chunk in chunks:

        chunk_id = f"document_{document_id}_chunk_{chunk['chunk_index']}"

        collection.upsert(
            ids=[chunk_id],
            documents=[chunk["chunk_text"]],
            metadatas=[{
                "document_id": document_id,
                "chunk_index": chunk["chunk_index"],
                "page_number": chunk["page_number"]
            }]
        )

    return len(chunks)


# Search document chunks
def search_chunks(question, limit=3):

    collection = get_collection()

    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[question],
        n_results=min(limit, collection.count())
    )

    matches = []

    for i in range(len(results["documents"][0])):

        matches.append({
            "chunk_text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i]
        })

    return matches
