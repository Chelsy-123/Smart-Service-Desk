# rag/classify.py

import json
from google import genai
from django.conf import settings
from .prompts import CLASSIFICATION_PROMPT

genai.configure(api_key=settings.GEMINI_API_KEY)

MODEL = "gemini-1.5-flash"


def classify_ticket(query: str):
    prompt = CLASSIFICATION_PROMPT.format(query=query)

    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(prompt)

    try:
        data = json.loads(response.text)

        # Defensive validation (very important in real systems)
        request_type = data.get("request_type", "IT")
        priority = data.get("priority", "MEDIUM")

        return {
            "request_type": request_type,
            "priority": priority
        }

    except Exception:
        # 🔹 Intelligent fallback (instead of static IT + MEDIUM)
        query_lower = query.lower()

        if any(word in query_lower for word in [
            "access", "login", "permission", "denied", "blocked", "unauthorized"
        ]):
            priority = "HIGH"
        else:
            priority = "MEDIUM"

        return {
            "request_type": "IT",
            "priority": priority
        }
