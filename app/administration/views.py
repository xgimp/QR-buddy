from django.views.generic import ListView

from qr_pair.models import ChatRoom


class RoomListView(ListView):
    model = ChatRoom
