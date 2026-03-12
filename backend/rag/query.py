from .confidence import calculate_confidence
from .llm import generate_answer_with_confidence
from .vectorstore import search_documents


def rag_query(query: str):
    # 1️⃣ Retrieve documents
    docs = search_documents(query)

    if not docs:
        return {
            "answer": "I couldn't find relevant information.",
            "confidence": 0.0,
            "sources": []
        }

    contents = [d["content"] for d in docs]
    similarities = [d["score"] for d in docs]
    sources = [d["source"] for d in docs]

    # 2️⃣ Generate answer + LLM confidence
    answer, llm_confidence = generate_answer_with_confidence(
        query=query,
        context=contents
    )

    # 3️⃣ Calculate final confidence
    confidence = calculate_confidence(similarities, llm_confidence)

    return {
        "answer": answer,
        "confidence": confidence,
        "sources": sources
    }
