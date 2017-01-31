from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from eleccion.models import *

class AutenticacionForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password']
        widgets={'password': forms.PasswordInput(),}

class circunscripcionForm(forms.ModelForm):
	class Meta:
		model = circunscripcion
		fields= ['nombre','mesas']

class mesaForm(forms.ModelForm):
	class Meta:
		model = mesa
		fields= ['nombre','partidos']

class CirForm(forms.ModelForm):
	class Meta:
		model = circunscripcion
		fields= ['mesas']
