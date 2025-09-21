from rest_framework import serializers
from .models import User, Conversation, Message

# ✅ User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # explicit CharField for input
    email = serializers.CharField()  # explicit CharField for email

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'password', 'phone_number', 'role']


# ✅ Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()  # explicit CharField

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']


# ✅ Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()  # dynamic field for nested messages

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']

    def get_messages(self, obj):
        # returns all messages for this conversation using the MessageSerializer
        messages = obj.messages.all().order_by('sent_at')
        return MessageSerializer(messages, many=True).data
