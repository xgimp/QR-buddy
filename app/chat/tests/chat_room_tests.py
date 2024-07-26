import json
from urllib.parse import urljoin
from uuid import UUID

import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from chat.tests.chat_room_factory import ChatRoomFactory, MessageFactory
from qr_pair.models import QRCode


@pytest.mark.django_db
class TestChatRoom:
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
        assert response.status_code == 200
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

        assert non_existing_user_id not in (
            chat_room.get_qr_codes.first().pk,
            chat_room.get_qr_codes.last().pk,
        )
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
        assert chat_room.get_qr_codes.count() == 2

    def test_cant_assign_more_than_two_qr_codes_to_room(self, chat_room):
        """
        Test that we cannot assign more than two QR Codes to chat room.
        """
        with pytest.raises(ValidationError) as exc_info:
            # 'chat_room' already got 2 QR codes generated for it, so this should fail
            QRCode.objects.create(chat_room=chat_room)
        assert exc_info.type is ValidationError
        assert exc_info.value.args[0] == "Already got 2 QR codes for this room"

    def test_qr_models_clean_method(self, chat_room):
        """
        Test that clean() raises ValidationError if room already got two QR codes assigned.
        So user cant assign additional (third) QR code in Django Admin.
        """
        with pytest.raises(ValidationError) as exc_info:
            # 'chat_room' already got 2 QR codes generated for it, so this should fail
            QRCode(chat_room=chat_room).clean()
        assert exc_info.type is ValidationError
        assert exc_info.value.args[0] == "Already got 2 QR codes for this room"

    def test_message_str_representation(self, chat_room):
        """
        Test that string representation of Message model instance is in intended format.
        """
        sender = chat_room.get_qr_codes.first()
        message = MessageFactory.create(message="hi", sender=sender)
        assert str(message) == f"[{sender}]:{message.message}"

    def test_chat_room_str_representation(self, chat_room):
        """
        Test that string representation of ChatRoom model instance is in intended format.
        """
        assert str(chat_room) == f"Chat Room ID: {chat_room.pk}"

    def test_chat_room_link(self, chat_room):
        """
        Test that chat_room_link() returns valid (chat) room URL path.
        """
        qr_code = chat_room.get_qr_codes.first()
        assert qr_code.chat_room_link == urljoin(
            settings.DOMAIN, f"/chat/{chat_room.pk}/{qr_code.pk}/"
        )

    def test_qr_svg_string(self, chat_room):
        """
        Test that qr_svg_string() returns SVG string.
        """
        # TODO: improve this
        svg_str = chat_room.get_qr_codes.first().qr_svg_string
        assert "<svg", "</svg>" in svg_str

    def test_chat_form_valid_message(self):
        """
        Test that SendMessage returns 'valid message' JSON if user enters valid message.
        """
        client = Client()

        post_url = reverse("chat:send_message")
        response = client.post(path=post_url, data={"message": "test"})
        data = json.loads(response.content)
        assert response.status_code == 200
        assert data["valid"] is True

    def test_chat_form_invalid_message(self):
        """
        Test that SendMessage returns 'invalid message' JSON if user enters invalid (empty) message.
        """
        client = Client()

        post_url = reverse("chat:send_message")
        response = client.post(path=post_url, data={"message": ""})
        data = json.loads(response.content)
        assert response.status_code == 200
        assert data["valid"] is False
        assert data["errors"]["message"][0] == "This field is required."
