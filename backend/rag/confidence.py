# rag/confidence.py

def calculate_confidence(similarity_scores, llm_confidence: float):
    """
    similarity_scores: List[float]  (0–1)
    llm_confidence: float (0–1)
    """

    if not similarity_scores:
        return 0.0

    avg_similarity = sum(similarity_scores) / len(similarity_scores)

    # Number of documents signal
    doc_factor = min(len(similarity_scores) / 5, 1.0)

    # Weighted confidence score
    confidence = (
        (avg_similarity * 0.6) +
        (doc_factor * 0.2) +
        (llm_confidence * 0.2)
    )

    return round(confidence, 2)
