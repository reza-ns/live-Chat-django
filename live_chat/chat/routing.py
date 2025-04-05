from django.urls import path
from chat import consumers


websocket_urlpatterns = [
    path('ws/chat/<str:room>/', consumers.ChatRoomConsumer.as_asgi())
]