# from django.views.generic import DetailView, ListView
#
# from qr_pair.models import ChatRoom
#
#
# class ChatRoomDetailView(DetailView):
#     model = ChatRoom
#
#
# class ChatRoomListView(ListView):
#     model = ChatRoom
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"
