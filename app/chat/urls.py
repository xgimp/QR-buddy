from django.urls import path

from .views import room


urlpatterns = [
    path("<str:room_name>/<str:user_id>", room, name="room"),
]
