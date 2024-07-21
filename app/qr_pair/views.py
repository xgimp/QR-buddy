from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from qr_pair.models import ChatRoom


class ChatRoomDetailView(LoginRequiredMixin, DetailView):
    model = ChatRoom


class ChatRoomListView(LoginRequiredMixin, ListView):
    model = ChatRoom
