from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from eleccion import views
from eleccion.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GestorElectoral.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^circunscripciones/$', listCircunscripciones.as_view(), name='Listar circunscripciones'),
    url(r'^add/circunscripcion/$', addCircunscripcion.as_view(), name='Anadir circunscripcion'),
    url(r'^update/circunscripcion/(?P<nombre>[0-9a-zA-Z]+)/$', updateCircunscripcion.as_view(), name='Editar circunscripcion'),
    url(r'^delete/circunscripcion/(?P<nombre>[0-9a-zA-Z]+)/$', deleteCircunscripcion.as_view(), name='Borrar circunscripcion'),
    url(r'^mesas/(?P<nombre>[0-9a-zA-Z]+)/$', views.listMesas, name='Listar mesas'),
    url(r'^mesa/(?P<nombre>[0-9a-zA-Z]+)/$', views.mesa, name='Detalle mesa'),
    url(r'^add/mesa/$', views.addMesa, name='Anadir mesa'),
    url(r'^update/mesa/(?P<nombre>[0-9a-zA-Z]+)/$', views.updateMesa, name='Editar mesa'),
    url(r'^add/resultado/$', views.addResultado, name='Anadir resultado'),
    url(r'^asignacion/circunscripcion/(?P<nombre>[0-9a-zA-Z]+)/$', views.asignacion, name='Asignaciones'),
    url(r'^$', TemplateView.as_view(template_name = 'index.html'), name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.userLogin, name='Login'),
    url(r'^logout/$', views.userLogout, name='Logout'),
)
