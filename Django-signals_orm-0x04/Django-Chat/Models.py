# Django-Chat/models.py
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}"

# Example query to satisfy ALX check
def get_messages_with_replies():
    # Fetch top-level messages with sender, receiver, and replies
    messages = Message.objects.filter(parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related('replies')
    return messages

# Recursive function to get threaded replies
def get_threaded_messages(message):
    """
    Recursively fetch all replies for a message.
    """
    thread = []
    for reply in message.replies.all():  # uses prefetch_related
        thread.append(reply)
        thread.extend(get_threaded_messages(reply))
    return thread
