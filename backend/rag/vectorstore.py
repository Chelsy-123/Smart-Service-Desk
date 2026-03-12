# rag/vectorstore.py

import os
import pickle
import numpy as np
import faiss

from django.conf import settings
from .embeddings import embed_text

VECTOR_DIR = os.path.join(settings.BASE_DIR, "rag", "vector_db")
INDEX_PATH = os.path.join(VECTOR_DIR, "faiss.index")
META_PATH = os.path.join(VECTOR_DIR, "metadata.pkl")


def _load_index():
    if not os.path.exists(INDEX_PATH):
        raise RuntimeError("FAISS index not found. Run ingest_documents() first.")

    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata


def search_documents(query: str, top_k: int = 3):
    """
    Search vector DB for relevant documents
    """
    index, metadata = _load_index()

    query_embedding = embed_text(query)
    query_embedding = np.array([query_embedding]).astype("float32")

    scores, indices = index.search(query_embedding, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue

        doc = metadata[idx]
        results.append({
            "content": doc["content"],
            "source": doc["source"],
            "category": doc.get("category"),
            "priority": doc.get("priority"),
            "score": float(score)
        })

    return results
