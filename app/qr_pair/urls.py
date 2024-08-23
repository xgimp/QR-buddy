from django.urls import path

from qr_pair.views import IndexView


app_name = "qr_pair"
urlpatterns = [
    path("", IndexView.as_view(), name="index_view"),
]
