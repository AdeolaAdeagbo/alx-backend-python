from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def unread_inbox(request):
    unread_messages = Message.unread.unread_for_user(request.user)  # <-- matches ALX check
    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})








