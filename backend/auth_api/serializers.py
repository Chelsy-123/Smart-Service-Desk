from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from users.models import Agent

User = get_user_model()


# -------------------------
# USER REGISTRATION
# -------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# -------------------------
# AGENT CREATION (ADMIN)
# -------------------------
class AgentCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    agent_name = serializers.CharField()
    department = serializers.CharField()

    def create(self, validated_data):
        department = validated_data.pop('department')
        agent_name = validated_data.pop('agent_name')
        password = validated_data.pop('password')

        # Create User
        user = User(**validated_data)
        user.set_password(password)
        user.is_staff = True  # Mark as staff
        user.save()

        # Assign Group (Department)
        group, _ = Group.objects.get_or_create(name=department)
        user.groups.add(group)

        # Create Agent Profile
        agent = Agent.objects.create(
            user=user,
            agent_name=agent_name
        )
        return agent
    
    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists")
        return data



class AgentResponseSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    groups = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = ["id", "agent_name", "username", "email", "groups"]

    def get_groups(self, obj):
        return list(obj.user.groups.values_list("name", flat=True))
