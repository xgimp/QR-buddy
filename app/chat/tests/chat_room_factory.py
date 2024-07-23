import factory
from factory.django import DjangoModelFactory

from chat.models import Message
from qr_pair.models import ChatRoom, QRCode


class ChatRoomFactory(DjangoModelFactory):
    class Meta:
        model = ChatRoom


class QrCodeFactory(DjangoModelFactory):
    class Meta:
        model = QRCode

    chat_room = factory.SubFactory(ChatRoomFactory)


class MessageFactory(DjangoModelFactory):
    class Meta:
        model = Message

    sender = factory.SubFactory(QrCodeFactory)
