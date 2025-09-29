# messaging/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Prefetch

# --- Custom Manager for Unread Messages ---
class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Returns unread top-level messages for a specific user.
        Optimized with .only(), select_related, and prefetch_related.
        """
        return self.filter(receiver=user, read=False, parent_message__isnull=True)\
                   .only('id', 'sender', 'content', 'timestamp', 'parent_message')\
                   .select_related('sender', 'receiver')\
                   .prefetch_related('replies')


# --- Message Model ---
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='replies'
    )

    # Managers
    objects = models.Manager()  # default
    unread = UnreadMessagesManager()  # custom manager

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}"


# --- MessageHistory Model ---
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Edit of {self.message.id} by {self.edited_by}"


# --- Example Queries for Threaded Conversations ---
def get_top_level_messages_with_replies():
    """
    Fetch top-level messages (parent_message is None)
    with sender, receiver, and all replies efficiently.
    """
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
