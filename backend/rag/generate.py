from google import genai
from django.conf import settings
from .vectorstore import search_documents
from .prompts import RAG_ANSWER_PROMPT

# Initialize Gemini client (NEW SDK)
client = genai.Client(api_key=settings.GEMINI_API_KEY)

MODEL = "gemini-flash-latest"


CONFIDENCE_THRESHOLD = 0.25


def generate_rag_answer(question: str):
    # 1️⃣ Retrieve relevant docs
    docs = search_documents(question, top_k=3)

    if not docs:
        return {
            "answer": "I couldn’t find relevant information. Please create a support ticket.",
            "confidence": 0.0,
            "sources": []
        }

    # 2️⃣ Build context
    context = "\n\n".join(
        f"Source: {d['source']}\n{d['content']}"
        for d in docs
    )

    # 3️⃣ Prompt
    prompt = RAG_ANSWER_PROMPT.format(
        context=context,
        question=question
    )

    # 4️⃣ Generate answer (NEW SDK)
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    answer = response.text.strip()

    # 5️⃣ Confidence score
    confidence = round(docs[0]["score"], 2)

    # Do NOT append ticket messages here
    # # Let frontend decide using suggest_create_ticket
    pass


    return {
        "answer": answer,
        "confidence": confidence,
        "sources": [d["source"] for d in docs],
        "category": docs[0].get("category"),
        "priority": docs[0].get("priority")
    }
