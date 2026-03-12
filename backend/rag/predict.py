from .vectorstore import search_documents
from collections import Counter

# -------------------------------
# Configuration
# -------------------------------
CONFIDENCE_THRESHOLD = 0.35
HIGH_PRIORITY_TYPES = {"SECURITY", "IT", "ACCESS"}
CRITICAL_KEYWORDS = {"vpn", "access", "login", "breach", "unauthorized"}


def predict_ticket_fields(description: str):
    """
    Predict request_type and priority using RAG metadata.

    This function is SAFE to use for:
    - Normal ticket creation (UI / API)
    - Chatbot-based ticket creation

    No LLM calls. Deterministic behavior.
    """

    docs = search_documents(description, top_k=3)

    if not docs:
        return {
            "request_type": "GENERAL",
            "priority": "LOW",
            "confidence": 0.0,
            "sources": []
        }

    # -------------------------------
    # Aggregate signals
    # -------------------------------
    categories = []
    priorities = []
    scores = []
    sources = []

    for doc in docs:
        categories.append(doc.get("category", "GENERAL"))
        priorities.append(doc.get("priority", "MEDIUM"))
        scores.append(doc.get("score", 0.0))
        sources.append(doc.get("source"))

    # -------------------------------
    # Majority voting
    # -------------------------------
    request_type = Counter(categories).most_common(1)[0][0]
    priority = Counter(priorities).most_common(1)[0][0]

    # -------------------------------
    # Confidence computation
    # -------------------------------
    confidence = round(sum(scores) / len(scores), 2)

    # -------------------------------
    # Rule-based safety overrides
    # -------------------------------

    # 1️⃣ Low confidence → downgrade
    if confidence < CONFIDENCE_THRESHOLD:
        priority = "LOW"

    # 2️⃣ Critical keywords → elevate
    if any(word in description.lower() for word in CRITICAL_KEYWORDS):
        if request_type in HIGH_PRIORITY_TYPES:
            priority = "HIGH"

    # 3️⃣ Never auto-escalate HR to HIGH
    if request_type == "HR" and priority == "HIGH":
        priority = "MEDIUM"

    return {
        "request_type": request_type,
        "priority": priority,
        "confidence": confidence,
        "sources": sources
    }
