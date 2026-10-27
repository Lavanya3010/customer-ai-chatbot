from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text: str) -> list[float]:
    """Convert text into a numerical vector."""
    embedding = model.encode(text)
    return embedding.tolist()