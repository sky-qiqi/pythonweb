# chat_api/urls.py
from django.urls import path
from .views import ChatAPIView

urlpatterns = [
    path('chat/', ChatAPIView.as_view(), name='chat_api'),
]