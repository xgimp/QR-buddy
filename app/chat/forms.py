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

    def clean_message(self):
        message = self.cleaned_data["message"]

        if not message:
            raise ValueError("message cannot be empty")
        if len(message) < 10:
            raise ValueError("message must be at leas 10 characters long")

        return message
