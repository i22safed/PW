from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your models here.

class Circunscripcion(models.Model):
	nombreCir = models.CharField(max_length=30, unique=True)
	nEscanos = models.IntegerField(null=False)
	slug = models.SlugField(blank=True, null=True)
	id = models.AutoField(primary_key=True)
	
	def __unicode__(self):
		return self.nombreCir

class Mesa(models.Model):
	id = models.AutoField(primary_key=True)
	circunscripcion = models.ForeignKey(Circunscripcion)
	nombreMesa = models.CharField(max_length=30)

	def __unicode__(self):
		return self.nombreMesa
	
class Partido(models.Model):
	
	nombrePartido = models.CharField(max_length=30, unique=True)
	nVotos = models.IntegerField()

	def __unicode__(self):
		return self.nombrePartido

class Resultado(models.Model):
	partido = models.ForeignKey(Partido)
	mesa = models.ForeignKey(Mesa)

