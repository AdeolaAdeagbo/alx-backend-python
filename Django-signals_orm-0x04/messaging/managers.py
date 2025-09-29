# messaging/managers.py
from django.db import models
from django.db.models import Prefetch
from .models import Message

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Returns unread top-level messages for a specific user.
        Optimized with .only(), select_related, and prefetch_related.
        """
        return self.filter(receiver=user, read=False, parent_message__isnull=True)\
                   .only('id', 'sender', 'content', 'timestamp', 'parent_message')\
                   .select_related('sender', 'receiver')\
                   .prefetch_related(Prefetch('replies', queryset=Message.objects.all()))
