from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView

from qr_pair.models import ChatRoom
from django.urls import reverse_lazy


class RoomListView(ListView):
    model = ChatRoom


class RoomCreateView(CreateView):
    model = ChatRoom
    fields = "__all__"
    success_url = reverse_lazy("administration:room_list")


class RoomDeleteView(DeleteView):
    model = ChatRoom
    pk_url_kwarg = "room_pk"
    success_url = reverse_lazy("administration:room_list")
