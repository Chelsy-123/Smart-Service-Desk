import json
from google import genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

MODEL = "gemini-1.5-flash"


def generate_answer_with_confidence(query, context):
    prompt = f"""
You are a support assistant.

Context:
{chr(10).join(context)}

User question:
{query}

Respond in JSON ONLY:
{{
  "answer": "...",
  "confidence": 0.0 to 1.0
}}
"""

    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(prompt)

    try:
        data = json.loads(response.text)
        return data["answer"], float(data["confidence"])
    except Exception:
        return (
            "I'm not fully sure about the answer. Please create a ticket.",
            0.3
        )
