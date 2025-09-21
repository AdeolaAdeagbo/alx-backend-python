# messaging_app/chats/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, ConversationViewSet, MessageViewSet

# Create the router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Include the router URLs
urlpatterns = [
    path('', include(router.urls)),
]
