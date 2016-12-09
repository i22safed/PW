# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Post

# Aqui se deben de poner los elementos para la administración del admin

admin.site.register(Post)
