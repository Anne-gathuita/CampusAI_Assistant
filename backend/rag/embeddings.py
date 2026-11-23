
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embedding(text):
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    embedding = model.encode(text)

    return embedding.tolist()


def generate_embeddings(texts):
    if not texts:
        return []

    embeddings = model.encode(texts)

    return embeddings.tolist()
