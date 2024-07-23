from factory.django import DjangoModelFactory

from qr_pair.models import ChatRoom


class ChatRoomFactory(DjangoModelFactory):
    class Meta:
        model = ChatRoom
