import json

import pytest
from asgiref.sync import sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator

from chat.consumers import save_chat_message
from chat.routing import websocket_urlpatterns
from chat.tests.chat_room_factory import ChatRoomFactory

# TODO: create communicator fixture?


async def test_socket_connection_is_successful_if_user_authorized():
    """
    Test that websocket connection is successful if user is authorized.
    """
    room = "439ce734-1baf-4a1e-abee-77e5a2149cc5"
    qr_id = "ac8297e7-c41d-4b94-a88e-673087269166"
    url_path = f"/ws/chat/{room}/{qr_id}/"
    communicator = WebsocketCommunicator(URLRouter(websocket_urlpatterns), url_path)

    communicator.scope["user"] = "ac8297e7-c41d-4b94-a88e-673087269166"
    connected, _ = await communicator.connect()
    assert connected

    # Close
    await communicator.disconnect()


async def test_socket_connection_is_closed_if_user_not_authorized():
    """
    Test that websocket connection is closed if user is not authorized.
    """
    room = "439ce734-1baf-4a1e-abee-77e5a2149cc5"
    qr_id = "ac8297e7-c41d-4b94-a88e-673087269166"
    url_path = f"/ws/chat/{room}/{qr_id}/"

    communicator = WebsocketCommunicator(URLRouter(websocket_urlpatterns), url_path)
    assert not communicator.scope.get("user")

    # user_id must be in communicator.scope["user"] for user to be authenticated
    # therefore connect() should fail
    connected, _ = await communicator.connect()
    assert not connected

    # Close
    await communicator.disconnect()


@pytest.mark.django_db
async def test_socket_connection_send_message():
    """
    Test that authenticated user can send message.
    """
    room = await sync_to_async(ChatRoomFactory.create)()
    qr_to_chat_room = await room.get_qr_codes.afirst()
    url_path = f"/ws/chat/{room.pk}/{qr_to_chat_room}/"

    communicator = WebsocketCommunicator(URLRouter(websocket_urlpatterns), url_path)
    communicator.scope["user"] = str(qr_to_chat_room.pk)
    connected, _ = await communicator.connect()
    assert connected

    message_to_send = json.dumps(
        {"message": "hi", "sender_id": str(qr_to_chat_room.pk)}
    )

    await communicator.send_to(text_data=message_to_send)
    response = await communicator.receive_output()
    assert json.loads(response["text"])["message"] == "hi"
    assert json.loads(response["text"])["sender_id"] == str(qr_to_chat_room.pk)

    # Close
    await communicator.disconnect()


@pytest.mark.django_db
def test_save_message_value_error_if_room_name_does_not_exist():
    """
    Test that save_chat_message() if nonexistent chat room ID is given.
    """
    nonexistent_room_name = "ac8297e7-c41d-4b94-a88e-673087269166"
    nonexistent_sender = "ac8297e7-c41d-4b94-a88e-673087269166"
    with pytest.raises(ValueError) as exc_info:
        save_chat_message(
            room_name=nonexistent_room_name, sender=nonexistent_sender, message="test"
        )
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "chat room does not exists"


@pytest.mark.django_db
def test_save_message_value_error_if_sender_does_not_exist():
    """
    Test that save_chat_message() if nonexistent sender is given.
    """
    existing_room_name = ChatRoomFactory.create()
    nonexistent_sender = "ac8297e7-c41d-4b94-a88e-673087269166"

    with pytest.raises(ValueError) as exc_info:
        save_chat_message(
            room_name=str(existing_room_name.pk),
            sender=nonexistent_sender,
            message="test",
        )
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "Sender does not exists"
