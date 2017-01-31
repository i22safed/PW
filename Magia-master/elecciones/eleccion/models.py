
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class partidos(models.Model):
	nombre = models.CharField(max_length = 100)

	def __unicode__(self):
		return self.nombre

class mesa(models.Model):
	nombre = models.CharField(max_length = 100)
	partidos = models.ManyToManyField(partidos)
	
	def __unicode__(self):
		return self.nombre

class circunscripcion(models.Model):
	nombre = models.CharField(max_length = 100)
	mesas = models.ManyToManyField(mesa)
	
	def __unicode__(self):
		return self.nombre

class resultado(models.Model):
	partido = models.ForeignKey(partidos, related_name='partido')
	mesa = models.ForeignKey(mesa, related_name='mesa')
	resultado =  models.IntegerField(default=0)

	def __unicode__(self):
		return self.resultado
