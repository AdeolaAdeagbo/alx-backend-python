# messaging/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Prefetch

@login_required
def sent_messages(request):
    """
    Fetch top-level messages sent by the current user,
    with all replies prefetched.
    """
    replies_prefetch = Prefetch('replies', queryset=Message.objects.all())

    messages = Message.objects.filter(sender=request.user, parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related(replies_prefetch)

    context = {
        'messages': messages
    }
    return render(request, 'messaging/sent_messages.html', context)


