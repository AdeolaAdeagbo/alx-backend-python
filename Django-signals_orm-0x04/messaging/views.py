# messaging/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def unread_inbox(request):
    """
    Display only unread messages for the logged-in user,
    optimized with .only() and select_related()
    """
    # Using the custom manager + .only() + select_related
    unread_messages = Message.unread.unread_for_user(request.user)

    return render(request, 'messaging/unread_inbox.html', {
        'messages': unread_messages
    })


@login_required
def all_messages(request):
    """
    Fetch all top-level messages with their replies
    using prefetch_related and select_related for optimization
    """
    from django.db.models import Prefetch

    replies_prefetch = Prefetch('replies', queryset=Message.objects.all())

    top_messages = Message.objects.filter(parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related(replies_prefetch)\
        .only('id', 'sender', 'receiver', 'content', 'timestamp', 'parent_message')

    return render(request, 'messaging/all_messages.html', {
        'messages': top_messages
    })










