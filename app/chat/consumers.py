import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.auth import is_permitted
from chat.models import Message
from qr_pair.models import ChatRoom, QRCode


# https://stackoverflow.com/questions/64188904/django-channels-save-messages-to-database
class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def can_join(self, room_name, user_id) -> bool:
        return is_permitted(room_name=room_name, user_id=user_id)

    @database_sync_to_async
    def save_chat_message(self, message, sender):
        chat_room = ChatRoom.objects.get(id=self.room_name)
        sndr = QRCode.objects.get(id=sender, chat_room=chat_room)
        return Message.objects.create(sender=sndr, message=message)

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]

        self.room_group_name = f"chat_{self.room_name}"

        if not self.can_join(self.room_name, self.user_id):
            await self.disconnect(403)
            return

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        """
        Leave room group
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        """
        Receive message from WebSocket
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender_id"]

        # It is necessary to await creation of messages
        new_msg = await self.save_chat_message(message=message, sender=sender)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": new_msg.message,
                "sender_id": str(new_msg.sender),
            },
        )

    async def chat_message(self, event):
        """
        Receive message from room group
        """
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {"message": event["message"], "sender_id": event["sender_id"]}
            )
        )
