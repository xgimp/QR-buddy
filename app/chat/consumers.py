import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Message
from qr_pair.models import ChatRoom, QRCode


def save_chat_message(room_name, message, sender):
    """
    Saves user's message to the database.
    """
    chat_room_exists = ChatRoom.objects.filter(id=room_name).exists()

    if not chat_room_exists:
        raise ValueError("chat room does not exists")

    chat_room = ChatRoom.objects.get(id=room_name)
    sender_exists = QRCode.objects.filter(id=sender, chat_room=chat_room).exists()

    if not sender_exists:
        raise ValueError("Sender does not exists")

    sndr = QRCode.objects.get(id=sender, chat_room=chat_room)
    return Message.objects.create(sender=sndr, message=message)


# https://stackoverflow.com/questions/64188904/django-channels-save-messages-to-database
class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None
        self.user = None
        self.room_name = None

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.user = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_group_name = f"chat_{self.room_name}"

        _user = self.scope.get("user")

        if not _user:
            return await self.close(reason="not authorized")

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
        new_msg = await database_sync_to_async(save_chat_message)(
            room_name=self.room_name, message=message, sender=sender
        )

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
