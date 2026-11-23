
from sentence_transformers import SentenceTransformer


# Lightweight model suitable for semantic text search
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embedding(text):
    """
    Convert a piece of text into a numerical embedding.
    """

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    embedding = model.encode(text)

    return embedding.tolist()


def generate_embeddings(texts):
    """
    Convert multiple text chunks into numerical embeddings.
    """

    if not texts:
        return []

    embeddings = model.encode(texts)

    return embeddings.tolist()
