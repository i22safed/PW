from django import forms
from entregas.models import *

from django.forms import ModelForm

class NewDestForm(ModelForm):
	direccion = forms.CharField()
	ciudad = forms.CharField()
	distancia = forms.IntegerField()

	class Meta:
		model = Destinatario
		fields = ['direccion', 'ciudad', 'distancia']

	def __init__(self, *args, **kwargs):
		super(NewDestForm, self).__init__(*args, **kwargs)
		self.fields['direccion'].label = "Direccion"
		self.fields['ciudad'].label = "Ciudad"
		self.fields['distancia'].label = "Distancia"

class NewPaqueteForm(ModelForm):
	contenido = forms.CharField()
	valor = forms.IntegerField()

	class Meta:
		model = Paquete
		fields = ['contenido', 'valor', 'destinatario']




