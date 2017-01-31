from django.forms import ModelForm
from django_markdown.widgets import MarkdownWidget
from django import forms
from blog.models import Entry, Comentario, Tag, Mensaje

class ComentarioForm(ModelForm):
	class Meta:
		model = Comentario

		fields = ('title', 'body')

class EntradaForm(ModelForm):
	body = forms.CharField(widget=MarkdownWidget())
	class Meta:
		model = Entry

		fields = ('title', 'body', 'tags')

	

class TagsForm(ModelForm):
	class Meta:
		model = Tag

class MensajeForm(ModelForm):
	class Meta:
		model = Mensaje

		fields = ('title', 'body')