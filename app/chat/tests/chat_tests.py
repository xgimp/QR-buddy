from uuid import UUID

import pytest
from django.core.exceptions import ValidationError
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from chat.tests.chat_room_factory import ChatRoomFactory
from qr_pair.models import QRCode


@pytest.mark.django_db
class TestChat:
    @pytest.fixture
    def chat_room(self):
        return ChatRoomFactory.create()

    def test_room_view(self, chat_room):
        """
        Test that right template is used.
        """
        client = Client()

        chat_room_qr = chat_room.get_qr_codes.first()
        chat_room_url = reverse(
            "chat:room", kwargs={"room_name": chat_room.pk, "user_id": chat_room_qr.id}
        )
        response = client.get(chat_room_url)
        assertTemplateUsed(response=response, template_name="chat/room.html")

    def test_non_existing_user_cant_access_chat(self, chat_room):
        """
        Test that user that can't access room that is not paired with his QR Code.
        """
        client = Client()
        non_existing_user_id = UUID("2e9cd1e8-969b-4e15-bb9c-18d8d2e8d003")
        chat_room_url = reverse(
            "chat:room",
            kwargs={"room_name": chat_room.pk, "user_id": non_existing_user_id},
        )
        response = client.get(chat_room_url)

        assert not non_existing_user_id == chat_room.pk
        assert response.status_code == 404

    def test_user_can_access_chat(self, chat_room):
        """
        Test that user that can access room that is paired with his QR Code.
        """
        client = Client()

        chat_room_qr = chat_room.get_qr_codes.first()
        chat_room_url = reverse(
            "chat:room", kwargs={"room_name": chat_room.pk, "user_id": chat_room_qr.id}
        )
        response = client.get(chat_room_url)
        assert response.status_code == 200

    def test_room_is_created_with_two_qr_codes(self, chat_room):
        """
        Test that chat room is created with exactly two QR Codes.
        """
        assert len(chat_room.get_qr_codes) == 2

    def test_can_assign_more_than_two_qr_codes_to_room(self, chat_room):
        """
        Test that we cannot assign more than two QR Codes to chat room.
        """
        with pytest.raises(ValidationError) as exc_info:
            # 'chat_room' already got 2 QR codes generated for it, so this should fail
            QRCode.objects.create(chat_room=chat_room)
        assert exc_info.type is ValidationError
        assert exc_info.value.args[0] == "Already got 2 QR codes for this room"
