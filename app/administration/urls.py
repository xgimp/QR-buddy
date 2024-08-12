from django.urls import path

from .views import RoomListView


app_name = "administration"
urlpatterns = [
    path("rooms", RoomListView.as_view(), name="room_list"),
]
