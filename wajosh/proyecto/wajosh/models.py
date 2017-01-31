from django.db import models
from django.contrib.auth.models import User
from django import forms
#from localflavor.fr.forms import FRPhoneNumberField
#from localflavor.es.forms import ESIdentityCardNumberField

from django.forms import ModelForm, Textarea
from datetime import date
import datetime

from django.conf import settings
# from django.conf import settings
# Create your models here.
from django.contrib.auth.forms import UserCreationForm

"""
Spanish-specific Form helpers
"""

class UserProfile(User):
	avatar=models.ImageField(upload_to='imgProfiles', verbose_name='Imagen', blank=True)
	provincia=models.ForeignKey('Provincia')
	ciudad=models.CharField(max_length=50, blank=True)
	#nif = ESIdentityCardNumberField( blank=True)




#class Usuario(models.Model):
#	nombre=models.CharField(max_length=20)
#	edad=models.IntegerField()

#	def __unicode__(self):
#		return self.nombre


class Anuncio(models.Model):
	titulo=models.CharField(max_length=50)
	fecha=models.DateTimeField(default=datetime.datetime.now)
	#propietario=models.ForeignKey(UserProfile, verbose_name='propietario', related_name='anuncio')
	propietario=models.ForeignKey(User)
	texto=models.TextField(max_length=450)
	#precio=models.IntegerField()
	cambio=models.TextField(max_length=450)
	provincia=models.ForeignKey('Provincia')
	categoria=models.ForeignKey('Categoria')
	imagen=models.ImageField(upload_to='imgAnuncios', verbose_name='Imagen', blank=True)



	def __unicode__(self):
		return self.titulo


class Comentario(models.Model):
	texto=models.TextField(max_length=200, help_text='Comenta...', verbose_name='Comentario')
	propietario=models.ForeignKey(User)
	anuncio=models.ForeignKey(Anuncio)
	fecha=models.DateTimeField(default=datetime.datetime.now)

	def __unicode__(self):
		return self.texto


class Provincia(models.Model):
	nombre=models.CharField(max_length=50, unique=True)

	def __unicode__(self):
		return self.nombre

class Categoria(models.Model):
	nombre=models.CharField(max_length=50, unique=True)

	def __unicode__(self):
		return self.nombre

class Mensaje(models.Model):
	fromu = models.ForeignKey(User, related_name='fromu', blank=True, null = True)
	to = models.ForeignKey(User, related_name='to', blank=True, null = True)
	#date = models.DateField(auto_now_add=True, blank = True)
	fecha=models.DateTimeField(default=datetime.datetime.now)
	texto = models.TextField()
	leido = models.BooleanField(default=True)
	
class Distribucion(models.Model):
	correo=models.EmailField()

	def __unicode__(self):
		return self.correo