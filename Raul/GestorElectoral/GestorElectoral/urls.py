from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView, ListView
from eleccion.views import CirListView, FormCircunscripcion, EditarCircunscripcion, BorrarCircunscripcion, Logearse
from django.contrib.auth.decorators import login_required, permission_required

admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'GestorElectoral.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^listaCircunscripcion/$', CirListView.as_view(template_name='listaCircunscripcion.html'), name='Circunscripcion-list'),
    url(r'^addCircunscripcion/$',FormCircunscripcion.as_view()),
    url(r'^editarCircunscripcion/(?P<pk>[-\w]+)/$', EditarCircunscripcion.as_view()),
    url(r'^borrarCircunscripcion/(?P<pk>[-\w]+)/$', BorrarCircunscripcion.as_view()),
  	url(r'^addMesa/$', 'eleccion.views.AddMesa', name = 'addMesa'),
    url(r'^listaMesa/$', 'eleccion.views.ListaMesa', name = 'listaMesa'),
    url(r'^login/$', 'eleccion.views.Logearse'),
    url(r'^salir/$', 'eleccion.views.LogOut'),
    url(r'^detalle/(?P<idmesa>\S+)$', 'eleccion.views.DetallesMesa'),
    url(r'^editar/(?P<idmesa>\S+)$', 'eleccion.views.editarMesa'),
    url(r'^usuario/nuevo/$', 'eleccion.views.Logearse', name="nuevousuario"),

)

