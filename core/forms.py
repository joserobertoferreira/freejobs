from django import forms
from django.conf import settings
from django.core.mail import send_mail


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Digite seu nome'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu email'})
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu telefone'}),
    )
    address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu endereço'}),
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Digite sua mensagem'})
    )

    def send_email(self):
        # Send email using the self.cleaned_data dictionary
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        phone = self.cleaned_data['phone']
        address = self.cleaned_data['address']
        message = self.cleaned_data['message']

        send_mail(
            f'Mensagem de {name} <{email}>',
            f'Telefone: {phone}\nEndereço: {address}\n\nMensagem: {message}',
            email,
            [settings.CONTACT_EMAIL],
        )
