import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Message
from qr_pair.models import ChatRoom, QRCode


# https://stackoverflow.com/questions/64188904/django-channels-save-messages-to-database
class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_chat(self, message, sender):
        chat_room = ChatRoom.objects.get(id=self.room_name)
        sndr = QRCode.objects.get(id=sender, chat_room=chat_room)
        return Message.objects.create(sender=sndr, message=message)

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

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
        sender = text_data_json["sender"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "message": message, "sender": sender},
        )

    async def chat_message(self, event):
        """
        Receive message from room group
        """

        # It is necessary to await creation of messages
        new_msg = await self.create_chat(
            message=event["message"], sender=event["sender"]
        )
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {"message": new_msg.message, "sender": str(new_msg.sender)}
            )
        )
