import uuid
from urllib.parse import urljoin

import segno

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Q

from chat.models import Message


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @transaction.atomic
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        while QRCode.objects.filter(chat_room=self).count() < 2:
            QRCode.objects.create(chat_room=self)
        super().save()

    @property
    def get_qr_codes(self):
        """
        Return QR codes that have access to this room
        """
        return self.paired_qr.filter(chat_room=self)

    def __str__(self):
        return f"Chat Room ID: {self.id}"


class QRCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="paired_qr"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if QRCode.objects.filter(chat_room=self.chat_room).count() == 2:
            raise ValidationError("Already got 2 QR codes for this room")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if QRCode.objects.filter(chat_room=self.chat_room).count() == 2:
            raise ValidationError("Already got 2 QR codes for this room")
        super().save()

    @property
    def matching_qr(self):
        """
        Returns the other QR from the pair
        """
        return self.chat_room.paired_qr.exclude(id=self.id).first()

    @property
    def qr_svg_string(self) -> str:
        """
        Returns QR Code SVGimage as a string
        """
        qr = segno.make(self.chat_room_link)
        return qr.svg_inline(scale=5)

    @property
    def chat_room_link(self):
        """
        Returns chat Room URL
        """
        return urljoin(settings.DOMAIN, f"/chat/{self.chat_room.id}/{self.id}/")

    @property
    def chat_history(self):
        """
        Return Chat history for room based on sender ID
        """
        history = Message.objects.filter(Q(sender=self) | Q(sender=self.matching_qr))
        return history.order_by("sent_at")

    def __str__(self):
        return f"{self.id}"
