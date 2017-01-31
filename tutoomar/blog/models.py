from django.db import models
from django.contrib.auth.models import User
from datetime import date

class articulo(models.Model):
    titulo = models.CharField(max_length=70)
    fecha = models.DateField(default = date.today)
    texto = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vista = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo

# Create your models here.
