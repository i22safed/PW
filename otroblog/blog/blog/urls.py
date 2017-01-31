from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$','ablog1.views.index'),                                                  #Pagina principal
    url(r'^articulo/(?P<idArticulo>.*)/$','ablog1.views.un_articulo'),                #Entrada concreta
    url(r'^articulos/(?P<idUsuario>.*)/$','ablog1.views.articulo_usuario'),           #Entradas por usuario
    url(r'^articulo_categoria/(?P<idCategoria>.*)/$','ablog1.views.articulo_categoria'),    #Entrada por categoria
    url(r'^salir/$','ablog1.views.salir'),                                            #Cerrar sesion
    url(r'^entrar/$','ablog1.views.entrar'),                                          #Identificarse
    url(r'^nuevo_articulo/$','ablog1.views.nuevo_articulo'),                          #Nueva entrada
    url(r'^modificar_articulo/(?P<idArticulo>.*)/$','ablog1.views.modificar_articulo'), #Modificar entrada
    url(r'^nuevo_usuario/$','ablog1.views.nuevo_usuario'),                            #Registrar usuario
    url(r'^nuevo_comentario/(?P<idArticulo>.*)/$','ablog1.views.nuevo_comentario'),   #Nuevo comentario
    url(r'^modificar_comentario/(?P<idArticulo>.*)/(?P<idComentario>.*)/$','ablog1.views.modificar_comentario'), #Modificar comentario
    url(r'^borrar_comentario/(?P<idArticulo>.*)/(?P<idComentario>.*)/$','ablog1.views.borrar_comentario'),  #Borrar comentario
    url(r'^borrar_articulo/(?P<idArticulo>.*)/$','ablog1.views.borrar_articulo'),     #Borrar articulo y todos sus comentarios
    url(r'^nueva_categoria/$','ablog1.views.nueva_categoria'),                        #Nueva categoria
    url(r'^nuevo_blog/$','ablog1.views.nuevo_blog'),                                  #Nuevo blog
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
