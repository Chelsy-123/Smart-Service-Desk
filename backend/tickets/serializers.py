from rest_framework import serializers
from django.conf import settings
from tickets.models import (
    Ticket,
    TicketMessage,
    TicketAssignment,
    TicketFeedback,
    TicketAILog
)
from users.models import Agent

#_______________________________________________________________________________________________________

# Serializers for Ticketing System
#Ticket Serializer (Create + Read)
class TicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    assigned_agent = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'user',
            'assigned_agent',
            'subject',
            'description',
            'request_type',
            'priority',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['request_type', 'priority', 'status', 'assigned_agent', 'created_at', 'updated_at']
#📌 Why

# User is auto-assigned from request
# Status/agent controlled by backend
# Safe for end users
#_______________________________________________________________________________________________________

#Ticket Message (Chat) Serializer

class TicketMessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = TicketMessage
        fields = [
            'id',
            'sender_type',
            'sender',
            'message',
            'created_at'
        ]
        read_only_fields = ['sender_type', 'sender', 'created_at']

    def get_sender(self, obj):
        if obj.sender_type == 'USER' and obj.sender_user:
            return obj.sender_user.username
        if obj.sender_type == 'AGENT' and obj.sender_agent:
            return obj.sender_agent.agent_name
        return None
#  Clean chat UI support
# No exposed internal IDs
#_______________________________________________________________________________________________________


#Ticket Assignment Serializer (Agent only)
class TicketAssignmentSerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(source='agent.agent_name', read_only=True)

    class Meta:
        model = TicketAssignment
        fields = ['id', 'ticket', 'agent', 'agent_name', 'assigned_at']
        read_only_fields = ['assigned_at']
#_______________________________________________________________________________________________________

#Ticket Feedback Serializer
class TicketFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketFeedback
        fields = ['rating', 'comments', 'submitted_at']
        read_only_fields = ['submitted_at']
#_______________________________________________________________________________________________________

#AI Classification Log (Read-only)
class TicketAILogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAILog
        fields = '__all__'
        read_only_fields = fields
#Only for admin / debugging
# Never writable via API