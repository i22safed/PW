from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings

from django.conf.urls.static import static

from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'proyecto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
   	url(r'^$', 'wajosh.views.home', name='home'),

   	url(r'^anuncios/$', 'wajosh.views.listar_anuncios', name='a'),
    url(r'^btitulo/', 'wajosh.views.busquedaTitulo'),
    url(r'^bprovincia/', 'wajosh.views.busquedaProvincia'),
    url(r'^bcategoria/', 'wajosh.views.busquedaCategoria'),

   	url(r'^anuncios/nuevo$', 'wajosh.views.nuevo_anuncio', name='nuevo_anuncio'),
    url(r'^balias/', 'wajosh.views.busquedaAlias'),
    url(r'^bprovinciaU/', 'wajosh.views.busquedaProvinciaU'),


    url(r'^usuarios/$', 'wajosh.views.lista_usuarios', name='b'),

    url(r'^usuarios/nuevo$', 'wajosh.views.nuevo_usuario', name='asasda'),

    url(r'^contacto/$', 'wajosh.views.contacto', name='contacto'),

    url(r'^ingresar/$', 'wajosh.views.ingresar', name='login'),

    url(r'^privado/$', 'wajosh.views.privado', name='privado'),
        
    url(r'^cerrar/$', 'wajosh.views.cerrar', name='cerrar_sesion'),

        # url(r'^blog/', include('blog.urls')),

    url(r'^usuario/mizona/(?P<id_usuario>\d+)$', 'wajosh.views.miZona', name='zonausuario'),

    url(r'^verAnuncio/(?P<id_anuncio>\d+)$', 'wajosh.views.verAnuncio', name='Ver Anuncio'),

    url(r'^comentar/(?P<id_anuncio>\d+)$', 'wajosh.views.comentarios'),
    url(r'^verAnuncio/eliminarComentario/(?P<id_comentario>\d+)$', 'wajosh.views.eliminarComentario'),

    url(r'^eliminarAnuncio/(?P<id_anuncio>\d+)$', 'wajosh.views.eliminarAnuncio', name='EliminarAnuncio'),

    url(r'^editarAnuncio/(?P<id_anuncio>\d+)$', 'wajosh.views.editarAnuncio'),

    url(r'^usuario/mizona/clasificados/(?P<id_usuario>\d+)$', 'wajosh.views.clasificados', name='mis anuncios'),

    url(r'^usuario/mizona/editarPerfil/(?P<id_usuario>\d+)$', 'wajosh.views.editarPerfil'),

    url(r'^usuario/mizona/eliminarCuenta/(?P<id_usuario>\d+)$', 'wajosh.views.eliminarCuenta', name='deleteuser'),


    # Mensajes
    url(r'^usuario/mizona/buzon/$', 'wajosh.views.buzon'),
    url(r'^usuario/mizona/enviarMensaje/(?P<id_usuario>\d+)$', 'wajosh.views.enviarMensaje'),
    url(r'^usuario/mizona/buzon/mensaje/(?P<mensaje_id>\d+)$', 'wajosh.views.mensajeDetail'),
    url(r'^usuario/mizona/buzon/enviados/$', 'wajosh.views.mensajesEnviados'),
    url(r'^usuario/mizona/buzon/mensaje/eliminar/(?P<id_mensaje>\d+)$', 'wajosh.views.eliminarMensaje', name='eliminarMensaje'),


    url(r'^suscribete/$', 'wajosh.views.listaDistribucion'),
    #url(r'^categorias/$', TemplateView.as_view(template_name="categorias.html")),
    url(r'^categorias/$', 'wajosh.views.categorias'),



    url(r'^admin/', include(admin.site.urls)),

        # Activamos la url de los mediafiles
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),

    
)#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
