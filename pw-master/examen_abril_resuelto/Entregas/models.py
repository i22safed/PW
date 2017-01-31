from django.db import models
from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.

class Destinatario (models.Model):
	nombre = models.CharField (max_length = 128)
	direccion = models.CharField (max_length = 128)
	ciudad = models.CharField (max_length = 128)
	codigo_postal = models.IntegerField ()
	def __unicode__(self):
		return (self.nombre)

class Paquete (models.Model):
	destinatarioReceptor = models.ForeignKey(Destinatario)
	contenido = models.CharField (max_length = 128)
	valor = models.IntegerField()
	
	def __unicode__(self):
		return (self.contenido)


class Ruta(models.Model):
	nombredelaruta = models.CharField(max_length=100)	
	descripcion=models.CharField(max_length=200, blank=True)
	fecha=models.DateTimeField(auto_now_add = True)
	paquete = models.ForeignKey(Paquete)

	def __unicode__(self):
		return (self.nombredelaruta)

