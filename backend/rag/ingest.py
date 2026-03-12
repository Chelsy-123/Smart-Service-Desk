# rag/ingest.py

import os
import pickle
import faiss
import numpy as np
from django.conf import settings
from .embeddings import embed_text

VECTOR_DIR = os.path.join(settings.BASE_DIR, "rag", "vector_db")
INDEX_PATH = os.path.join(VECTOR_DIR, "faiss.index")
META_PATH = os.path.join(VECTOR_DIR, "metadata.pkl")

os.makedirs(VECTOR_DIR, exist_ok=True)

def ingest_documents():
    documents_dir = os.path.join(settings.BASE_DIR, "rag", "rag_docs")

    embeddings = []
    metadata = []

    for filename in os.listdir(documents_dir):
        filepath = os.path.join(documents_dir, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            continue

        vector = embed_text(content)

        embeddings.append(vector)
        metadata.append({
            "content": content,        # 🔥 REQUIRED
            "source": filename,         # filename
            "category": "IT",           # optional
            "priority": "MEDIUM"        # optional
        })

    dimension = len(embeddings[0])
    index = faiss.IndexFlatIP(dimension)
    index.add(np.array(embeddings).astype("float32"))

    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print(f"Ingested {len(metadata)} documents successfully")
