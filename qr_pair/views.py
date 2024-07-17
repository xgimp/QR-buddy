from django.views.generic import DetailView, ListView

from qr_pair.models import QRCode


class QRCodeDetailView(DetailView):
    model = QRCode


class QRCodeListView(ListView):
    model = QRCode