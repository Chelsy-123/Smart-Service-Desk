from django.contrib import admin
from .models import Ticket, TicketMessage, TicketAssignment, TicketFeedback, TicketAILog
# Register your models here.
admin.site.register(Ticket)
admin.site.register(TicketMessage)
admin.site.register(TicketAssignment)
admin.site.register(TicketFeedback)
admin.site.register(TicketAILog)