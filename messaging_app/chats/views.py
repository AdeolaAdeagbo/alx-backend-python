from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer

# ✅ ViewSet for Conversation
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    # Optional: custom action to get all messages for a conversation
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

# ✅ ViewSet for Message
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']
