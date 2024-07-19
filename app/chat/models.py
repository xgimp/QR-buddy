from django.db import models


class Message(models.Model):
    message = models.TextField()
    sender = models.ForeignKey("qr_pair.QRCode", on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"[{self.sender}]:{self.message}"
