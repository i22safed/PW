from django.conf.urls import patterns, include, url
from Entregas import views
from .views import *

urlpatterns = patterns ('',
	
	#Destinatarios
	url (r'^verDestinatario', views.verDestinatarios, name='Ver Destinatario'),
	url (r'^addDestinario', views.addDestinatario, name='Anadir Destinario'),
	url (r'^destinatario/(?P<destinatario_id>\d+)', views.DetallesDestinatario, name='Detalles Destinatario'),
	
	#Paquetes
	url (r'^verPaquetes', views.verPaquetes, name='Ver Paquetes'),
	url (r'^addPaquete', views.addPaquete, name='Anadir Paquete'),
	url (r'^paquete/(?P<paquete_id>\d+)', views.detallesPaquete, name='Detalles Paquete'),
	url (r'^editarPaquete/(?P<Paquete_id>\d+)$', views.editarPaquete, name='Editar Paquete'),

	#Rutas (Como funciones)
	 #url (r'^verRuta', views.verRuta, name='Ver Ruta'),
	 #url (r'^addRuta', views.addRuta, name='Anadir Ruta'),
	 #url (r'^ruta/(?P<ruta_>\w+)$',views.detallesRuta, name='Detalles Ruta'),

	#Rutas (con Vistas basadas en clases)
	url (r'^verRuta', verRuta.as_view(), name='Ver Ruta'),
	url (r'^addRuta', addRuta.as_view(), name='Anadir Ruta'),
	url (r'^ruta/(?P<Ruta_id>\w+)$', detallesRuta.as_view(), name='Detalles Ruta'),
)
