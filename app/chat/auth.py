from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError
from django.http import Http404

from qr_pair.models import QRCode, ChatRoom


def is_permitted(room_name, user_id) -> bool:
    user_exists = QRCode.objects.filter(id=user_id).exists()
    room_exists = ChatRoom.objects.filter(id=room_name).exists()

    if not user_exists or not room_exists:
        return False

    user = QRCode.objects.get(id=user_id)
    room = ChatRoom.objects.get(id=room_name)

    return user.chat_room.id == room.id
