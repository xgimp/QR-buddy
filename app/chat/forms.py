from django import forms
from django.http import JsonResponse

from chat.models import Message


class ChatForm(forms.ModelForm):
    message = forms.CharField(
        label="message",
        widget=forms.TextInput(
            attrs={
                "placeholder": "enter message",
                "id": "chat-message-input",
                "aria-describedby": "invalid-helper",
            }
        ),
    )

    class Meta:
        model = Message
        fields = ("message",)

    def clean_message(self):
        message = self.cleaned_data["message"]

        if not message:
            raise forms.ValidationError("Message cannot be empty")
        if len(message) < 2:
            raise forms.ValidationError("message must be at least 2 characters long")
        return message
