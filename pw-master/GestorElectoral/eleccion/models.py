from django.db import models

# Create your models here.
class Circunscripcion(models.Model):
	escanos = models.IntegerField(default=0)
	nombre = models.CharField(max_length = 128, default= "Circunscripcion")
	def __unicode__(self):
		return self.nombre

class Mesa(models.Model):
	circunscripcion = models.ForeignKey(Circunscripcion)
	nombre = models.CharField(max_length = 128, default= "Mesa")
	def __unicode__(self):
		return self.nombre

class Partido(models.Model):
	nombre = models.CharField(max_length = 128, unique = True, default= "Partido")
	def __unicode__(self):
		return self.nombre

class Resultado(models.Model):
	partido = models.ForeignKey(Partido)
	mesa = models.ForeignKey(Mesa)
	votos = models.IntegerField(default=0)
	def __unicode__(self):
		return self.partido.nombre + ' ' + self.mesa.nombre
