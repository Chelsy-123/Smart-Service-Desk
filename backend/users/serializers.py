from rest_framework import serializers
from users.models import Admin, User, Agent, UserNotificationPreference
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    is_agent = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_superuser', 'is_staff', 'is_agent',]

    def get_is_agent(self, obj):
        return hasattr(obj, 'agent')


class AgentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Agent
        fields = ['id', 'agent_name', 'user', 'is_active']

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Admin
        fields = ['id', 'user']


class UserNotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotificationPreference
        fields = '__all__'
        read_only_fields = ['user']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("New passwords do not match")

        validate_password(data["new_password"])
        return data