from authentication.models import User
from rest_framework import serializers
from chat.models import Message
from chat.models import Settings

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='id', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='id', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']

class SettingsSerializer(serializers.ModelSerializer):
    key = serializers.CharField(max_length=100)
    value = serializers.CharField(max_length=100)

    class Meta:
        model = Settings
        fields = ['key', 'value']