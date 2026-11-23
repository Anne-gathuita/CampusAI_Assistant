
from rag.embeddings import generate_embedding

sample_text = (
    "Students must follow the official university "
    "examination regulations."
)

embedding = generate_embedding(sample_text)

print("EMBEDDING GENERATED SUCCESSFULLY!")
print("Number of numerical values:", len(embedding))
print("First five values:", embedding[:5])
