from django.urls import path

from .views import RoomListView, RoomCreateView, RoomDeleteView

app_name = "administration"
urlpatterns = [
    path("", RoomListView.as_view(), name="room_list"),
    path("rooms/add", RoomCreateView.as_view(), name="create_room"),
    path("rooms/delete/<str:room_pk>/", RoomDeleteView.as_view(), name="delete_room"),
]
