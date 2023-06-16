from django import forms
from app.models import Chat

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('Remetente', 'Telefone', 'Assunto', 'Mensagem')
