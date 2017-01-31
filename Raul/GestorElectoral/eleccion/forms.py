from django import forms
from .models import Circunscripcion, Mesa
from django.forms import ModelForm

class CircunscripcionForm(forms.ModelForm):

	class Meta:
		model = Circunscripcion
		fields = ['nombreCir', 'nEscanos']


class MesaForm(forms.ModelForm):

	class Meta:

			model = Mesa
			fields = ['circunscripcion', 'nombreMesa']
					



		