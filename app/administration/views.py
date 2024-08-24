from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView

from qr_pair.models import ChatRoom
from django.urls import reverse_lazy


class RoomListView(ListView):
    model = ChatRoom
    template_name = "administration/room_list.html"


class RoomCreateView(CreateView):
    model = ChatRoom
    template_name = "administration/add_room_form.html"
    fields = "__all__"
    success_url = reverse_lazy("administration:room_list")


class RoomDeleteView(DeleteView):
    model = ChatRoom
    template_name = "administration/room_confirm_delete.html"
    pk_url_kwarg = "room_pk"
    success_url = reverse_lazy("administration:room_list")
