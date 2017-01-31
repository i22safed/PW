from django.conf.urls import patterns, url
from . import views, feed
from blog.views import EntradasDia


urlpatterns = patterns(
	'',
	url(r'^feed/$', feed.LatestPosts(), name="feed"),
	url(r'^usuario/nuevo/$', views.nuevo_usuario, name="nuevousuario"),
	url(r'^$', views.BlogIndex, name="index"),
	url(r'^entry/(?P<slug>\S+)$', views.BlogDetail, name="entrydetail"),
	url(r'^comentar/(?P<id_entrada>\S+)$', views.nuevocomentario, name="comentar"),
	url(r'^publicar/$', views.nuevaentrada, name="nuevaentrada"),
	url(r'^user/$', views.panel_usuario),
	url(r'^ingresar/$', views.ingresar),
	url(r'^publicar/crear/tags/$', views.creartags),
	url(r'^cerrar/sesion/$', views.cerrarsesion),
	url(r'^mensajes/$', views.mensajes),
	url(r'^enviar/mensaje/$', views.enviarmensaje),
	url(r'^eliminar/mensaje/(?P<id_mensaje>\S+)$', views.eliminarmensaje),
	url(r'^editar/(?P<id_entrada>\S+)$', views.editarentrada),
	url(r'^delete_comment/(\d+)/$', views.delete_comment),
	url(r'^delete_comment/(\d+)/(\d+)$', views.delete_comment),
	url(r'^blog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})$', EntradasDia.as_view(), name='entradas'),
	url(r'^confirmacion/eliminar/entrada/(?P<id_entrada>\S+)$', views.eliminarentrada),
	url(r'^eliminar/entrada/(?P<id_entrada>\S+)$', views.confirmacioneliminar),
	#url(r'^entry/(?P<id_entrada>\d+)', views.comentarios),
)