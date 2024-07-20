from django.urls import path

from .views import room, SendMessage

app_name = "chat"
urlpatterns = [
    path("<str:room_name>/<str:user_id>", room, name="room"),
    path("send", SendMessage.as_view(), name="send_message"),
]
