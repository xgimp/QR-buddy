import uuid
import segno

from django.core.exceptions import ValidationError
from django.db import models, transaction


class QRMatch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    @transaction.atomic
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        while QRCode.objects.filter(pair=self).count() < 2:
            QRCode.objects.create(pair=self)
        super().save()

    def __str__(self):
        return f"match {self.id}"


class QRCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pair = models.ForeignKey(QRMatch, on_delete=models.CASCADE, related_name='paired_qr')

    def clean(self):
        if QRCode.objects.filter(pair=self.pair).count() == 2:
            raise ValidationError("Already got 2 QR codes")

    # def save(
    #     self, force_insert=False, force_update=False, using=None, update_fields=None
    # ):
    #     if QRCode.objects.filter(pair=self.pair).count() == 2:
    #         raise ValidationError("Already got 2 QR codes")
    #     super().save()

    @property
    def matching_qr(self):
        """
        Returns the other QR from the pair
        """
        return self.pair.paired_qr.exclude(id=self.id).first()

    @property
    def qr_svg_string(self) -> str:
        """
        Returns QR Code SVGimage as a string
        """
        qr = segno.make(str(self.id))
        return qr.svg_inline(scale=5)

    def __str__(self):
        return f"{self.id}"
