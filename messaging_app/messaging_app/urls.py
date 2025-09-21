from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include the chats app API URLs under /api/
    path('api/', include('chats.urls')),
]
