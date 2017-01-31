from django.contrib import admin


# Register your models here.
from ablog1.models import articulo
from ablog1.models import comentario
from ablog1.models import categoria
from ablog1.models import blog
admin.site.register(articulo)
admin.site.register(comentario)
admin.site.register(categoria)
admin.site.register(blog)