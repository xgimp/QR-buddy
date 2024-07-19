from django.urls import path

from qr_pair.views import ChatRoomDetailView, ChatRoomListView

app_name = "qr_pair"
urlpatterns = [
    path(
        "detail/<uuid:pk>", ChatRoomDetailView.as_view(), name="chat_room_detail_view"
    ),
    path("", ChatRoomListView.as_view(), name="chat_room_list_view"),
]
