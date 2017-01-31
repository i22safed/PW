from django.contrib import admin

# Register your models here.

#from wajosh.models import Poll, Choice

#admin.site.register(Poll)
#admin.site.register(Choice)

from wajosh.models import UserProfile, Anuncio, Comentario, Provincia, Categoria,Mensaje, Distribucion

admin.site.register(UserProfile)
admin.site.register(Anuncio)
admin.site.register(Comentario)
admin.site.register(Provincia)
admin.site.register(Categoria)
admin.site.register(Mensaje)
admin.site.register(Distribucion)