from django.urls import path
from rest_framework.routers import DefaultRouter
from tickets.views import TicketViewSet, TicketMessageViewSet, TicketFeedbackViewSet


router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='tickets')

urlpatterns = router.urls + [
    path(
        'tickets/<int:ticket_id>/messages/',
        TicketMessageViewSet.as_view({
            'get': 'list',
            'post': 'create'
        }),
        name='ticket-messages'
    ),

    path(
        'tickets/<int:ticket_id>/feedback/',
        TicketFeedbackViewSet.as_view({
            'get': 'list',
            'post': 'create'
        }),
        name='ticket-feedback'
    ),
]

# api endpoints:
# Action	        Endpoint
# Create ticket 	POST /api/tickets/tickets/
# List tickets	    GET /api/tickets/tickets/
# Chat messages 	GET /api/tickets/5/messages/
# Send message  	POST /api/tickets/5/messages/
# Submit feedback	POST /api/tickets/5/feedback/

# # TICKETS
# POST   /api/tickets/tickets/               → Create ticket
# GET    /api/tickets/tickets/               → My Tickets (created by logged-in user)

# # AGENT ONLY
# GET    /api/tickets/tickets/assigned/      → Assigned tickets (agent)

# # TICKET DETAILS
# GET    /api/tickets/tickets/<id>/           → Ticket details
# PATCH  /api/tickets/tickets/<id>/           → Agent updates status

# # MESSAGES
# GET    /api/tickets/tickets/<id>/messages/  → View messages
# POST   /api/tickets/tickets/<id>/messages/  → Send message

# # FEEDBACK
# POST   /api/tickets/tickets/<id>/feedback/  → Submit feedback
