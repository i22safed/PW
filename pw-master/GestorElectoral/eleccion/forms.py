from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from eleccion.models import *

class AuthenticationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class CircunscripcionForm(forms.ModelForm):
    class Meta:
        model = Circunscripcion
        fields = ['escanos', 'nombre']

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['circunscripcion', 'nombre']

class ResultadoForm(forms.ModelForm):
    class Meta:
        model = Resultado
        fields = ['partido', 'mesa', 'votos']
