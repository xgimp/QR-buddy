from uuid import UUID

from qr_pair.models import QRCode, ChatRoom


def is_valid_uuid(uuid_str: str, version=4) -> bool:
    """
    Helper function to validate UUID format
    """
    try:
        UUID(uuid_str, version=version)
    except ValueError:
        return False
    else:
        return True


def is_permitted(room_name, user_id) -> bool:
    # validate input data
    if not all((is_valid_uuid(room_name), is_valid_uuid(user_id))):
        return False

    user_exists = QRCode.objects.filter(id=user_id).exists()
    room_exists = ChatRoom.objects.filter(id=room_name).exists()

    if not user_exists or not room_exists:
        return False

    user = QRCode.objects.get(id=user_id)
    room = ChatRoom.objects.get(id=room_name)

    return user.chat_room.id == room.id
