from tickets.models import Ticket
from tickets.services.ticket_events import (
    handle_ticket_created,
    auto_assign_ticket
)

def create_ticket_via_chatbot(*, user, message, request_type, priority):
    ticket = Ticket.objects.create(
        user=user,
        subject="Created via Chatbot",
        description=message,
        request_type=request_type,
        priority=priority,
        status="OPEN"
    )

    # 🔔 These already trigger Redis emails in your system
    handle_ticket_created(ticket)
    auto_assign_ticket(ticket)

    return ticket
