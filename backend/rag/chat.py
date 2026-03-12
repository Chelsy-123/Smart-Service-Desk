# rag/chat.py

from google import genai
from django.conf import settings
from .retrieve import retrieve_context
from .prompts import RAG_SYSTEM_PROMPT

genai.configure(api_key=settings.GEMINI_API_KEY)

MODEL = "gemini-1.5-flash"

def rag_chat(query: str):
    context = retrieve_context(query)

    prompt = f"""
{RAG_SYSTEM_PROMPT}

DOCUMENTS:
{context}

USER QUESTION:
{query}
"""

    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(prompt)

    return {
        "answer": response.text,
        "has_context": bool(context.strip())
    }
