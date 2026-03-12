from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rag.predict import predict_ticket_fields
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status as drf_status
from tickets.models import Ticket, TicketMessage, TicketFeedback
from tickets.serializers import (
    TicketSerializer,
    TicketMessageSerializer,
    TicketFeedbackSerializer
)
from tickets.services.ticket_events import (
    handle_ticket_created,
    auto_assign_ticket
)
from common.permissions import IsOwnerOrAssignedAgent
from django.contrib.auth.models import Group


# =====================================================
# TICKET VIEWSET
# =====================================================
class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAssignedAgent]

    def get_queryset(self):
        user = self.request.user

        # ADMIN
        if user.is_superuser:
            return Ticket.objects.all().order_by("-created_at")

        # LIST VIEW
        if self.action == "list":
            return Ticket.objects.filter(user=user).order_by("-created_at")

        # DETAIL VIEW → allow lookup, permissions handle access
        return Ticket.objects.all()

    @action(detail=False, methods=["get"], url_path="assigned")
    def assigned_tickets(self, request):
        if not hasattr(request.user, "agent"):
            return Response([])

        tickets = Ticket.objects.filter(
            assigned_agent=request.user.agent
        ).order_by("-created_at")

        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)
    


        # =====================================================
    # AGENT: UPDATE TICKET STATUS
    # =====================================================
    @action(detail=True, methods=["patch"], url_path="status")
    def update_status(self, request, pk=None):
        user = request.user

        # Only agents can update status
        if not hasattr(user, "agent"):
            return Response(
                {"detail": "Only agents can update ticket status."},
                status=403
            )

        ticket = get_object_or_404(
            Ticket,
            id=pk,
            assigned_agent=user.agent
        )

        new_status = request.data.get("status")

        if not new_status:
            return Response(
                {"detail": "Status is required."},
                status=400
            )

        ticket.status = new_status
        ticket.save()

        serializer = self.get_serializer(ticket)
        return Response(serializer.data)
    # =====================================================
    # 🔹 CREATE TICKET (unchanged logic)
    def perform_create(self, serializer):
        description = serializer.validated_data.get("description")

        # -----------------------------
        # RAG-based prediction
        # -----------------------------
        prediction = predict_ticket_fields(description)

        ticket = serializer.save(
            user=self.request.user,
            request_type=prediction["request_type"],
            priority=prediction["priority"]
        )
        # -----------------------------
        handle_ticket_created(ticket)
        auto_assign_ticket(ticket)
        # ---------------------------------------------
        # FUTURE RAG / RULE ENGINE HOOK
        # ---------------------------------------------
        # For now: simple department-based assignment
        # Uses Django Groups (IT, HR, FAC, etc.)
        try:
            group = Group.objects.get(name=ticket.request_type)
            agent_user = (
                group.user_set
                .filter(agent__is_active=True)
                .select_related('agent')
                .first()
            )

            if agent_user:
                ticket.assigned_agent = agent_user.agent
                ticket.status = 'IN_PROGRESS'
                ticket.save()

        except Group.DoesNotExist:
            pass
        # ---------------------------------------------
class TicketMessageViewSet(viewsets.ModelViewSet):
    serializer_class = TicketMessageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAssignedAgent]

    def get_queryset(self):
        ticket = get_object_or_404(Ticket, id=self.kwargs['ticket_id'])
        self.check_object_permissions(self.request, ticket)
        return TicketMessage.objects.filter(ticket=ticket)

    def perform_create(self, serializer):
        ticket = get_object_or_404(Ticket, id=self.kwargs['ticket_id'])

        if hasattr(self.request.user, 'agent'):
            serializer.save(
                ticket=ticket,
                sender_type='AGENT',
                sender_agent=self.request.user.agent
            )
        else:
            serializer.save(
                ticket=ticket,
                sender_type='USER',
                sender_user=self.request.user
            )
# =====================================================
# TICKET FEEDBACK VIEWSET
# =====================================================
class TicketFeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = TicketFeedbackSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAssignedAgent]

    def get_queryset(self):
        ticket = get_object_or_404(Ticket, id=self.kwargs['ticket_id'])
        self.check_object_permissions(self.request, ticket)
        return TicketFeedback.objects.filter(ticket=ticket)

    def perform_create(self, serializer):
        ticket = get_object_or_404(Ticket, id=self.kwargs['ticket_id'])
        serializer.save(ticket=ticket)
#_______________________________________________________________________________________________________