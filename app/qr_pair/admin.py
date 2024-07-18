from django.contrib import admin

from qr_pair.models import QRCode, QRMatch

admin.site.register(QRCode)
admin.site.register(QRMatch)
