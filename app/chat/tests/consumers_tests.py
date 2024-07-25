import json

import pytest
from asgiref.sync import sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator

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
