# messaging/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Triggered before a Message is saved.
    If the message content has changed, save the old content in MessageHistory
    and mark the message as edited.
    """
    if instance.id:  # Only for existing messages (not new ones)
        try:
            old_message = Message.objects.get(id=instance.id)
        except Message.DoesNotExist:
            return  # Message doesn’t exist, probably new, do nothing

        if old_message.content != instance.content:
            # Save old content into MessageHistory
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content
            )
            # Mark message as edited
            instance.edited = True
