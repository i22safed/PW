from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class categoria(models.Model):
	nombre=models.CharField(max_length=50)
	def __unicode__(self):
		return self.nombre

class articulo(models.Model):
	titulo=models.CharField(max_length=50, null=False)
	cuerpo=models.TextField()
	usuario=models.ForeignKey(User, null=False)
	categoria=models.ForeignKey(categoria, null=True, blank=True)
	imagen=models.ImageField(blank=True, null=True, upload_to='Imagenes_Articulos/')
	fecha=models.DateTimeField(auto_now_add=True)
	fechaMod=models.DateTimeField(blank=True, null=True)
	def __unicode__(self):
		return self.titulo

class comentario(models.Model):
	texto=models.TextField()
	fecha=models.DateTimeField(auto_now_add=True)
	articulo=models.ForeignKey(articulo, null=False)
	usuario=models.ForeignKey(User)
	fechaMod=models.DateTimeField(blank=True, null=True)

class blog(models.Model):
	nombre=models.CharField(max_length=50)
	autor=models.CharField(max_length=50)
	url=models.URLField()
	def __unicode__(self):
		return self.nombre