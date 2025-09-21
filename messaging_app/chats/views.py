# messaging_app/chats/views.py
from rest_framework import viewsets, filters
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

# ✅ ViewSet for Conversations
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__username']  # search by usernames
    ordering_fields = ['created_at']
    ordering = ['-created_at']


# ✅ ViewSet for Messages
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['sender__username', 'message_body']  # search by sender or message
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']
