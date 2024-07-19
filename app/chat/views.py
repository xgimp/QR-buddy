from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import render

from qr_pair.models import ChatRoom, QRCode


def room(request, room_name, user_id):
    # TODO: refactor
    try:
        user = QRCode.objects.get(id=user_id)
    except (QRCode.DoesNotExist, ValidationError):
        raise Http404("User does not exists")

    try:
        room = ChatRoom.objects.get(id=room_name)
    except (ChatRoom.DoesNotExist, ValidationError):
        raise Http404("Chat room does not exist.")

    has_permission = user.chat_room.id == room.id
    if not has_permission:
        raise Http404("no permission")

    return render(
        request, "chat/room.html", {"room_name": str(room.id), "user_id": str(user.id)}
    )
