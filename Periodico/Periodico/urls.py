# -*- coding: utf-8 -*-

"""Periodico URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin


    # Para cada url de admin/ Django encontrará su correspondiente view para
    # ello necesitamos de expresiones regulares (regex):
    # ^ denota el principio del texto
    # $ denota el final del texto
    # \d representa un dígito
    # + indica que el ítem anterior debería ser repetido por lo menos una vez
    # () para encerrar una parte del patrón


urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'', include('principal.urls')),
]
