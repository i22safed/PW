from django.forms import ModelForm
from django import forms
from .models import * 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DestinatarioForm (forms.ModelForm):
	class Meta:
		model = Destinatario

class PaqueteForm (forms.ModelForm):
	class Meta:
		model = Paquete

class RutaForm (forms.ModelForm):
	class Meta:
		model = Ruta

class AuthenticationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


