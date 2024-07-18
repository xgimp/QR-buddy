from django.urls import path

from qr_pair.views import QRCodeDetailView, QRCodeListView

app_name = "qr_pair"
urlpatterns = [
    path("detail/<uuid:pk>", QRCodeDetailView.as_view(), name="qr_detail_view"),
    path("", QRCodeListView.as_view(), name="qr_list_view"),
]
