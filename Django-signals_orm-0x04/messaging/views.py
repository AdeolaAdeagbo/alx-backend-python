# messaging/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def unread_inbox(request):
    """
    Display only unread top-level messages for the logged-in user,
    optimized with select_related and only().
    """
    # Explicit query using manager and optimization
    unread_messages = Message.unread.for_user(request.user) \
                                   .select_related('sender', 'receiver') \
                                   .only('id', 'sender', 'receiver', 'content', 'timestamp')

    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})


@login_required
def inbox(request):
    """
    Display all messages received by the logged-in user (including read).
    Optimized for performance with select_related and prefetch_related for replies.
    """
    messages = Message.objects.filter(receiver=request.user, parent_message__isnull=True) \
                              .select_related('sender', 'receiver') \
                              .prefetch_related('replies') \
                              .only('id', 'sender', 'receiver', 'content', 'timestamp', 'parent_message')

    return render(request, 'messaging/inbox.html', {'messages': messages})


@login_required
def sent_messages(request):
    """
    Display all messages sent by the logged-in user.
    """
    sent = Message.objects.filter(sender=request.user) \
                          .select_related('receiver') \
                          .only('id', 'receiver', 'content', 'timestamp', 'parent_message') \
                          .prefetch_related('replies')

    return render(request, 'messaging/sent.html', {'messages': sent})






