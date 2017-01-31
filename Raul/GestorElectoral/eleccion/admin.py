from django.contrib import admin
from eleccion.models import Circunscripcion, Mesa, Partido, Resultado

admin.site.register(Circunscripcion)
admin.site.register(Mesa)
admin.site.register(Partido)
admin.site.register(Resultado)

# Register your models here.
