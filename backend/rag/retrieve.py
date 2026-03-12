# rag/retrieve.py

import numpy as np
from sentence_transformers import SentenceTransformer
from .vectorstore import load_vectorstore

# SAME MODEL AS INGESTION — VERY IMPORTANT
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def embed_query(text: str):
    embedding = model.encode(text)
    return np.array(embedding).astype("float32")

def retrieve_context(query: str, top_k: int = 3):
    index, metadata = load_vectorstore()
    query_embedding = embed_query(query)

    distances, indices = index.search(
        np.array([query_embedding]), top_k
    )

    contexts = []
    for idx in indices[0]:
        contexts.append(metadata[idx]["content"])

    return "\n\n".join(contexts)
