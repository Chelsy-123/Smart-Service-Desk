# rag/embeddings.py

from sentence_transformers import SentenceTransformer

# Lightweight, fast, free, production-safe embedding model
_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str):
    """
    Convert text into vector embedding
    """
    return _model.encode(text, normalize_embeddings=True).tolist()
