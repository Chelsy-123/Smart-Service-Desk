from django.urls import path
from chatbot.views import (
    ChatbotChatAPIView,
    ChatbotCreateTicketAPIView
)

urlpatterns = [
    path("chat/", ChatbotChatAPIView.as_view(), name="chatbot-chat"),
    path("create-ticket/", ChatbotCreateTicketAPIView.as_view(), name="chatbot-create-ticket"),
]
