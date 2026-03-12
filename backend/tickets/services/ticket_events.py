from django.utils import timezone
from django.contrib.auth.models import Group

from tickets.models import Ticket, TicketAssignment
from users.models import Agent
from notifications.models import NotificationEvent, NotificationLog


# ==================================================
# GENERIC NOTIFICATION TRIGGER
# ==================================================
from notifications.tasks import send_notification_async

def trigger_notification(event_code, ticket, recipient_user=None, extra_payload=None):
    try:
        event = NotificationEvent.objects.get(code=event_code, is_active=True)
    except NotificationEvent.DoesNotExist:
        return

    template = event.notificationtemplate_set.filter(is_active=True).first()
    if not template:
        return  # 🚫 No template → no notification

    payload = {
        "ticket_id": ticket.id,
        "subject": ticket.subject,
        "status": ticket.status,
        "priority": ticket.priority,
    }

    if extra_payload:
        payload.update(extra_payload)

    log = NotificationLog.objects.create(
        event=event,
        channel=template.channel,
        recipient_user=recipient_user,
        recipient_address=recipient_user.email if recipient_user else "",
        payload=payload,
        status="PENDING"
    )
    return log
    



# ==================================================
# TICKET CREATED
# ==================================================
def handle_ticket_created(ticket: Ticket):
    log=trigger_notification(
        event_code="TICKET_CREATED",
        ticket=ticket,
        recipient_user=ticket.user
    )
    if log:
        # ✅ Send asynchronously
        send_notification_async.delay(log.id)

# ==================================================
# AUTO ASSIGN AGENT (NEW)
# ==================================================
def auto_assign_ticket(ticket: Ticket):
    """
    Auto-assign ticket based on request_type (IT / HR / FAC)
    Uses Django Groups as departments
    """

    department = ticket.request_type  # IT / HR / FAC

    try:
        group = Group.objects.get(name=department)
    except Group.DoesNotExist:
        return None

    agent = (
        Agent.objects
        .filter(user__groups=group, is_active=True)
        .select_related("user")
        .first()
    )

    if not agent:
        return None

    old_status = ticket.status

    ticket.assigned_agent = agent
    ticket.status = "IN_PROGRESS"
    ticket.save()

    handle_ticket_assigned(ticket, agent)
    handle_ticket_status_change(ticket, old_status)

    return agent


# ==================================================
# TICKET ASSIGNED
# ==================================================
def handle_ticket_assigned(ticket: Ticket, agent: Agent):
    TicketAssignment.objects.create(
        ticket=ticket,
        agent=agent
    )
    # 🔔 Notify ticket owner
    user_log = trigger_notification(
        event_code="TICKET_ASSIGNED",
        ticket=ticket,
        recipient_user=ticket.user,
        extra_payload={
            "agent": agent.agent_name,
            "department": ticket.request_type
        }
    )
    if user_log:
        send_notification_async.delay(user_log.id)

       # 🔔 Notify agent (THIS WAS MISSING)
    agent_log = trigger_notification(
        event_code="TICKET_ASSIGNED_AGENT",
        ticket=ticket,
        recipient_user=agent.user,
        extra_payload={
            "agent": agent.agent_name,
            "department": ticket.request_type
        }
    )
    if agent_log:
        send_notification_async.delay(agent_log.id)


# ==================================================
# TICKET STATUS CHANGE
# ==================================================
def handle_ticket_status_change(ticket: Ticket, old_status: str):
    log = trigger_notification(
        event_code="TICKET_STATUS_CHANGED",
        ticket=ticket,
        recipient_user=ticket.user,
        extra_payload={
            "old_status": old_status,
            "new_status": ticket.status
        }
    )
    if log:
        send_notification_async.delay(log.id)
