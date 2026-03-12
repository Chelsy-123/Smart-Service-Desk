from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rag.predict import predict_ticket_fields
from rag.generate import generate_rag_answer
from chatbot.services.ticket_creator import create_ticket_via_chatbot
from tickets.services.ai_logger import log_ticket_ai_prediction


class ChatbotChatAPIView(APIView):
    """
    Chat ONLY:
    - RAG answer
    - Predict request_type & priority
    - DOES NOT create ticket
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get("message")

        if not message:
            return Response(
                {"error": "Message is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        rag_response = generate_rag_answer(message)
        prediction = predict_ticket_fields(message)
        CONFIDENCE_THRESHOLD = 0.35
        confidence = prediction["confidence"]

        return Response(
    {
        "chatbot_reply": rag_response["answer"],
        "predicted_request_type": prediction["request_type"],
        "predicted_priority": prediction["priority"],
        "confidence": confidence,
        "sources": rag_response.get("sources", []),

        # ✅ UX signals
        "suggest_create_ticket": confidence < CONFIDENCE_THRESHOLD,
        "auto_create_allowed": confidence >= CONFIDENCE_THRESHOLD
    },
    status=status.HTTP_200_OK
)

class ChatbotCreateTicketAPIView(APIView):
    """
    Ticket creation ONLY:
    - Requires user confirmation
    - Uses predicted fields
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        message = request.data.get("message")
        request_type = request.data.get("request_type")
        priority = request.data.get("priority")
        confidence = request.data.get("confidence")

        if not all([message, request_type, priority]):
            return Response(
                {"error": "Missing required fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ticket = create_ticket_via_chatbot(
            user=user,
            message=message,
            request_type=request_type,
            priority=priority
        )

        # Log AI decision
        log_ticket_ai_prediction(
            ticket=ticket,
            request_type=request_type,
            priority=priority,
            confidence=confidence
        )

        return Response(
            {
                "ticket_created": True,
                "ticket_id": ticket.id,
                "request_type": request_type,
                "priority": priority,
                "confidence": confidence
            },
            status=status.HTTP_201_CREATED
        )
