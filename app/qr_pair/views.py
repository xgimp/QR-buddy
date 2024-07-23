from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from qr_pair.models import ChatRoom


class ChatRoomDetailView(DetailView):
    model = ChatRoom


class ChatRoomListView(ListView):
    model = ChatRoom
