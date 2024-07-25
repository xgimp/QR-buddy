from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from chat.auth import is_permitted


class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # TODO: clean this monstrosity
        room_id = scope["path"].replace("/ws/chat/", "").split("/")[0]
        user_id = scope["path"].replace("/ws/chat/", "").split("/")[-2]

        is_permission_granted = await database_sync_to_async(is_permitted)(
            room_name=room_id, user_id=user_id
        )
        if is_permission_granted:
            scope["user"] = user_id
        return await self.app(scope, receive, send)
