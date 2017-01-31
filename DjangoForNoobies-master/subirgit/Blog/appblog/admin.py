from django.contrib import admin
from appblog.models import Entrada
from appblog.models import Comentario

# Register your models here.
admin.site.register(Entrada)
admin.site.register(Comentario)

