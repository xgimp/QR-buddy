from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import render

from qr_pair.models import ChatRoom


def room(request, room_name):
    try:
        room = ChatRoom.objects.get(id=room_name)
    except (ChatRoom.DoesNotExist, ValidationError):
        raise Http404("Chat room does not exist.")
    return render(request, "chat/room.html", {"room_name": str(room.id)})
