from django.contrib import admin
from trueque.models import Entrada
from trueque.models import Comentario
from trueque.models import UserProfile

# Register your models here.
admin.site.register(Entrada)
admin.site.register(Comentario)
