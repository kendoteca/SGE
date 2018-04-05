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

    def get_sounds():
        import os
        sounds = []
        for file in os.listdir("./static/"):
            if file.endswith((".mp3", ".mp4", ".wav", ".ogg")):
                sounds.append(
                    (os.path.join("/", file), file)
                )
        return sounds

    tipo_sonido_totem = forms.MultipleChoiceField(
        required=False,
        widget=forms.Select,
        choices=get_sounds(),
    )

    tipo_sonido_visualizador = forms.MultipleChoiceField(
        required=False,
        widget=forms.Select,
        choices=get_sounds(),
    )

    class Meta:
        model = Configuration
        fields = [
            'imprimir_promocion',
            'promocion_aleatoria',
            'generar_alarma_con_cantidad',
            'email_destino',
            'sonido_totem',
            'tipo_sonido_totem',
            'tipo_sonido_visualizador',
            'visualizador_standard',
        ]
