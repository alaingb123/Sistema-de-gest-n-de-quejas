
from django import forms
from .models import QuejaU
from django.contrib.auth import get_user_model
from datetime import date
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible
from django_recaptcha import fields
from django_recaptcha import widgets


class QuejaUForm(forms.ModelForm):
    captcha = fields.ReCaptchaField()

    # The dictionary is urlencoded and appended to the reCAPTCHA api url.

    class Meta:
        model = QuejaU
        exclude = ['fechaT','created', 'updated']
        fields = ['nombre_apellidos', 'asunto', 'telefono', 'direccion', 'argumento']

    nombre_apellidos = forms.CharField(
        label='Nombre y Apellidos',
        max_length=50
    )



    asunto = forms.CharField(
        label='Asunto',
        max_length=100
    )

    telefono = forms.IntegerField(
        label='Teléfono',
        required=False
    )

    direccion = forms.CharField(
        label='Dirección',
        max_length=255,
        required=False
    )

    argumento = forms.CharField(
        label='Argumento',
        max_length=10000,
        required=False,
        widget=forms.Textarea()
    )


    def clean_usuario(self):
        usuario = self.cleaned_data.get('usuario')
        if usuario is None:
            User = get_user_model()
            usuario = User.objects.get(pk=self.current_user.pk)
        return usuario

    @property
    def current_user(self):
        return self._current_user

    @current_user.setter
    def current_user(self, user):
        self._current_user = user


class FiltroQuejasForm(forms.Form):
    years = forms.ChoiceField(choices=[], label='Año')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        anos = QuejaU.objects.dates('created', 'year').distinct()
        choices = [(ano.year, str(ano.year)) for ano in anos]
        self.fields['years'].choices = choices
