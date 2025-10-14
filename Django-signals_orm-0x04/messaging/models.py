# messaging/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Prefetch

# --- Custom Manager for Unread Messages ---
class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Returns unread top-level messages for a specific user.
        Optimized with .only(), select_related, and prefetch_related.
        """
        return self.filter(
            receiver=user,
            read=False,
            parent_message__isnull=True
        ).only('id', 'sender', 'content', 'timestamp', 'parent_message')\
         .select_related('sender', 'receiver')\
         .prefetch_related('replies')


# --- Message Model ---
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

# --- MessageHistory Model ---
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

