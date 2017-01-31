from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.views.generic.list import ListView
from django import forms
from django.conf import settings
from datetime import datetime    

# Create your models here.

class UserProfile(User):
	photo = models.ImageField(upload_to='photos', verbose_name='photoprofile',  blank=True)
	ciudad = models.CharField(max_length = 50,  blank=True)
	amigos = models.ManyToManyField('self', symmetrical=True,  blank=True)

class Image(models.Model):
	titulo = models.CharField(max_length = 100, verbose_name='Titulo', unique=True)
	imagen = models.ImageField(upload_to='imagenes', verbose_name='imagen')
	autor = models.ForeignKey(User, blank = True, null = True, related_name='autor')
	repicers = models.ManyToManyField(User, blank = True, null = True, related_name='repicers')
	etiquetas = models.TextField(blank=True, null = True, default = None)
	date = models.DateField(default=datetime.now, blank = True)
	
class Comentario(models.Model):
	who = models.ForeignKey(User, blank=True, null = True)
	what = models.ForeignKey(Image, blank=True, null = True)
	texto = models.TextField()
	positivos = models.IntegerField(default = 0, blank=True) 
	date = models.DateField(auto_now_add=True, blank = True)

class Mensaje(models.Model):
	fromu = models.ForeignKey(User, related_name='fromu', blank=True, null = True)
	to = models.ForeignKey(User, related_name='to', blank=True, null = True)
	date = models.DateField(default=datetime.now, blank = True)
	texto = models.TextField()
	leido = models.BooleanField(default=True)

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

class busqueda(models.Model):
	busqueda = models.CharField(max_length = 50)
	
class UploadPicture(ModelForm):
	class Meta:
		model = Image
		fields = ['titulo', 'imagen', 'etiquetas', 'autor']

	def __init__(self, *args, **kwargs):
		super(UploadPicture, self).__init__(*args, **kwargs)
		self.fields['titulo'].label = "titulo"
		self.fields['imagen'].label = "imagen"
		self.fields['etiquetas'].label = "etiquetas"
		self.fields['autor'].label = "autor"

	def save(self, commit=True):
		image = super(UploadPicture, self).save(commit=False)
		if commit:
			image.save()
		return image

	
class imageList(ListView):
    model = Image

class userList(ListView):
    model = UserProfile

class comentarioList(ListView):
	model = Comentario

class mensajeList(ListView):
	model = Mensaje

class search(ModelForm):
	class Meta:
		model = busqueda
		fields = ['busqueda']

	def __init__(self, *args, **kwargs):
		super(search, self).__init__(*args, **kwargs)
		self.fields['busqueda'].label = "Busqueda"

class newComent(ModelForm):
	class Meta:
		model = Comentario	
		fields = ['texto', 'what', 'who']

class newMensaje(ModelForm):
	class Meta:
		model = Mensaje
		fields = ['texto','to', 'fromu']


