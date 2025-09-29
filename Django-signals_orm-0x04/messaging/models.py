# messaging/models.py
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  # Track if message was edited

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='history'
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"

# --- Example queries for threaded conversations ---

from django.db.models import Prefetch

def get_top_level_messages_with_replies():
    """
    Fetch top-level messages (parent_message is None)
    with sender, receiver, and all replies efficiently.
    """
    # Prefetch replies for each message
    replies_prefetch = Prefetch('replies', queryset=Message.objects.all())
    
    messages = Message.objects.filter(parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related(replies_prefetch)
    
    return messages

def get_threaded_replies(message):
    """
    Recursively fetch all replies for a message.
    """
    thread = []
    for reply in message.replies.all():  # uses prefetched data
        thread.append(reply)
        thread.extend(get_threaded_replies(reply))
    return thread

# Example usage:
# top_messages = get_top_level_messages_with_replies()
# for msg in top_messages:
#     print(msg.content)
#     all_replies = get_threaded_replies(msg)
#     for r in all_replies:
#         print(f"  ↳ {r.content}")
