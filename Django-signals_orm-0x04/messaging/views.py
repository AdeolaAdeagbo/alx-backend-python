# messaging/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def unread_inbox(request):
    """
    Display only unread top-level messages for the logged-in user.
    """
    # Using custom manager with .only() automatically inside manager
    unread_messages = Message.unread.for_user(request.user)

    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})




