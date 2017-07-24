from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Configuration


class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput(),
        }


class Configurations(ModelForm):
    class Meta:
        model = Configuration
        fields = [
            'imprimir_promocion',
            'promocion_aleatoria',
            'generar_alarma_con_cantidad',
            'email_destino',
            'sonido_totem',
            'visualizador_standard',
        ]

