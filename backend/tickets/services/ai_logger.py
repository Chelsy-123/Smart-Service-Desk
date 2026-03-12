from tickets.models import TicketAILog


def log_ticket_ai_prediction(
    *,
    ticket,
    request_type,
    priority,
    confidence,
    model_used="RAG + Gemini"
):
    """
    Persist AI prediction for auditing & debugging
    """
    TicketAILog.objects.create(
        ticket=ticket,
        model_used=model_used,
        predicted_request_type=request_type,
        predicted_priority=priority,
        confidence_score=confidence
    )
