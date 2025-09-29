# messaging/views.py
from django.shortcuts import render
from .models import Message
from django.contrib.auth.decorators import login_required

@login_required
def inbox(request):
    # Fetch top-level messages for the current user
    messages = Message.objects.filter(receiver=request.user, parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related('replies')
    
    context = {
        'messages': messages
    }
    return render(request, 'messaging/inbox.html', context)
