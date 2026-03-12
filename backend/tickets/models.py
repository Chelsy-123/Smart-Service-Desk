from django.db import models
from django.conf import settings

# ==================================================
# TICKET MODELS
# ==================================================

class Ticket(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('IT', 'IT'),
        ('HR', 'HR'),
        ('FAC', 'Facilities'),
    ]

    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]

    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('CLOSED', 'Closed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets'
    )

    assigned_agent = models.ForeignKey(
        "users.Agent",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )

    subject = models.CharField(max_length=255)
    description = models.TextField()

    request_type = models.CharField(max_length=10, choices=REQUEST_TYPE_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} ({self.status})"


# -----------------------------
# TICKET MESSAGE (CHAT)
# -----------------------------
class TicketMessage(models.Model):
    SENDER_TYPE_CHOICES = [
        ('USER', 'User'),
        ('AGENT', 'Agent'),
    ]

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender_type = models.CharField(max_length=10, choices=SENDER_TYPE_CHOICES)

    sender_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    sender_agent = models.ForeignKey(
        "users.Agent",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message for Ticket {self.ticket.id}"


# -----------------------------
# TICKET ASSIGNMENT HISTORY
# -----------------------------
class TicketAssignment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='assignments'
    )

    agent = models.ForeignKey(
        "users.Agent",
        on_delete=models.CASCADE
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.ticket.id} assigned to {self.agent.agent_name}"


# -----------------------------
# TICKET FEEDBACK
# -----------------------------
class TicketFeedback(models.Model):
    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        related_name='feedback'
    )

    rating = models.IntegerField()
    comments = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Ticket {self.ticket.id}"


# -----------------------------
# AI CLASSIFICATION LOG
# -----------------------------
class TicketAILog(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='ai_logs'
    )

    model_used = models.CharField(max_length=100)
    predicted_request_type = models.CharField(max_length=20)
    predicted_priority = models.CharField(max_length=20)
    confidence_score = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Log for Ticket {self.ticket.id}"
