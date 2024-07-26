import pytest
from unittest.mock import AsyncMock

from asgiref.sync import sync_to_async

from chat.middlewares import QueryAuthMiddleware
from chat.tests.chat_room_factory import ChatRoomFactory


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_middleware_with_valid_user():
    """
    Test that middleware adds user key to the scope if user is permitted to join the room.
    """
    app = AsyncMock()
    room = await sync_to_async(ChatRoomFactory.create)()
    qr_to_chat_room = await room.get_qr_codes.afirst()

    middleware = QueryAuthMiddleware(app)
    scope = {
        "path": f"/ws/chat/{room.pk}/{qr_to_chat_room.pk}/",
    }
    receive = AsyncMock()
    send = AsyncMock()

    await middleware(scope, receive, send)
    assert scope["user"] == str(qr_to_chat_room.pk)


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_middleware_with_invalid_user():
    """
    Test that 'user' key does not appear in scope if
    user is not permitted to join room or room_id is invalid.
    """
    app = AsyncMock()
    middleware = QueryAuthMiddleware(app)
    scope = {
        "path": "/ws/chat/fake_room/fake_user/",
    }
    receive = AsyncMock()
    send = AsyncMock()

    await middleware(scope, receive, send)
    assert not scope.get("user")
