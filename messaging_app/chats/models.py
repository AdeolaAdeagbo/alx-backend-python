# chats/models.py
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Use UUID as primary key
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Additional fields not in AbstractUser
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    def __str__(self):
        return f"{self.username} ({self.email})"
