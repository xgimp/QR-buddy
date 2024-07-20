from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView

from chat.auth import is_permitted
from chat.forms import ChatForm
from qr_pair.models import ChatRoom, QRCode


def room(request, room_name, user_id):
    if not is_permitted(room_name=room_name, user_id=user_id):
        raise Http404("user is not permitted")

    user = get_object_or_404(QRCode, id=user_id)
    room_to_join = get_object_or_404(ChatRoom, id=room_name)
    chat_form = ChatForm

    return render(
        request,
        "chat/room.html",
        {
            "room_name": str(room_to_join.id),
            "user_id": str(user.id),
            "history": list(user.chat_history.values()),
            "chat_form": chat_form,
        },
    )


class SendMessage(FormView):
    form_class = ChatForm
    http_method_names = ["post"]

    def form_valid(self, form):
        return JsonResponse({"valid": True})

    def form_invalid(self, form):
        return JsonResponse({"valid": False, "errors": form.errors})
