from django import forms
from app.models import Chat

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('sender', 'phone', 'subject', 'message')
