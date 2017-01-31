from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    # url(r'^Paqueteria/', include('Paqueteria.foo.urls')),
    url(r'^destinatarios$','entregas.views.DestinatariosView'),
    url(r'^destinatarios/new$','entregas.views.NewDestView'),
    url(r'^destinatarios/(?P<id_dest>\d+)$', 'entregas.views.DetallesDest'),
    url(r'^paquetes$','entregas.views.PaquetesView'),
    url(r'^paquetes/new$','entregas.views.NewPaqueteView'),
    url(r'^paquetes/(?P<id_paquete>\d+)$', 'entregas.views.DetallesPaquete'),
    url(r'^paquetes/(?P<id_paquete>\d+)/settings$', 'entregas.views.EditarPaquete'),
    
    url(r'^login$', 'entregas.views.login_view'),
    url(r'^register$', 'entregas.views.newUser'),
    url(r'^logout$', 'entregas.views.logout_view'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
