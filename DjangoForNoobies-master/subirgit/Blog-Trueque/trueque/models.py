from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.conf import settings
from datetime import datetime    

# Create your models here.
class Entrada(models.Model):
	titulo = models.CharField(max_length=100)
	telefono = models.CharField(max_length=100)
	deseado = models.CharField(max_length=100)
	fecha = models.DateTimeField(auto_now_add=True)
	vendedor = models.CharField(max_length=100)
	image = models.ImageField(upload_to='photos', verbose_name='productphoto',  blank=True)
	contenido = models.TextField()
	
	def __unicode__(self):
		return str(self.titulo)
		
class Comentario(models.Model):
	fechacreacion = models.DateTimeField(auto_now_add=True)
	autor = models.CharField(max_length=100)
	telefonoCo = models.CharField(max_length=100)
	mensaje = models.TextField()
	identrada = models.ForeignKey(Entrada)
	
	def __unicode__(self):
		return unicode("%s %s " %(self.identrada, self.mensaje[:60]))
		
class UserProfile(User):
	photo = models.ImageField(upload_to='photos', verbose_name='photoprofile',  blank=True)
	ciudad = models.CharField(max_length = 50,  blank=True)

class SingUpForm(ModelForm):
        password = forms.CharField(widget=forms.PasswordInput(render_value = False), required = True) 
	class Meta:
		model = UserProfile
		fields = ['username', 'password', 'first_name', 'photo', 'ciudad']	
		widgets = {
			'password': forms.PasswordInput(),		
		}

	def __init__(self, *args, **kwargs):
		super(SingUpForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = "username"
		self.fields['password'].label = "password"
		self.fields['first_name'].label = "first_name"
		self.fields['photo'].label = "photo"
		self.fields['ciudad'].label = "ciudad"

	def save(self, commit=True):
		user = super(SingUpForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user
