from django import forms

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
