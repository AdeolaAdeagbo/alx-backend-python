from rest_framework import serializers
from .models import User, Conversation, Message

# ✅ User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'phone_number',
            'role'
        ]
        extra_kwargs = {
            'password': {'write_only': True}  # Password won't be exposed in API responses
        }

    # Encrypt password when creating a new user
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# ✅ Message serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Nested info about sender

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'sent_at'
        ]


# ✅ Conversation serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # Nested participants
    messages = MessageSerializer(many=True, read_only=True)   # Nested messages

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages',
            'created_at'
        ]

