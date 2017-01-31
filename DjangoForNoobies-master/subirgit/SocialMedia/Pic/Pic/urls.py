from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.template import Template
from django.views.generic import TemplateView, CreateView
from django.conf.urls.static import static
from django.conf import settings
from Nav.models import UserProfile, SingUpForm

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$', 'Nav.views.indexUser'),
	url(r'^genericindex/$', TemplateView.as_view(template_name='index.html'), name='index'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^registrar/$', 'Nav.views.nuevoUser'),
    url(r'^login/$', 'Nav.views.ingresar'),
    url(r'^logout/$', 'Nav.views.cerrar'),
    url(r'^editar/$', 'Nav.views.editar'),
    url(r'^upload/$', 'Nav.views.UploadPictures'),
    url(r'^tablon/(?P<user_id>\d+)/$', 'Nav.views.imageList'),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
	url(r'^search/foto/(?P<etiqueta>\d+)/$', 'Nav.views.searchImage'),
	url(r'^search/foto/$', 'Nav.views.realizarBusqueda'),
	url(r'^search/user/$', 'Nav.views.buscaAmigos'),
	url(r'^search/user/(?P<username>\d+)/$', 'Nav.views.searchFriend'),
	url(r'^comentar/(?P<image_id>\d+)/$', 'Nav.views.comentar'),
	url(r'^comentar/(?P<img_id>\d+)/(?P<coment_id>\d+)/$', 'Nav.views.votar'),
	url(r'^repic/(?P<img_id>\d+)/(?P<user_id>\d+)/$', 'Nav.views.repic'),
	url(r'^addfriend/(?P<user_id>\d+)/$', 'Nav.views.addFriend'),
	url(r'^genericactivity/', 'Nav.views.allImg'),
	url(r'^actividad/$', 'Nav.views.actividad'),
	url(r'^enviarMensaje/$', 'Nav.views.enviarMensaje'),
	url(r'^mensaje/(?P<mensaje_id>\d+)/$', 'Nav.views.mensajeDetail'),
	url(r'^buzon/$', 'Nav.views.buzon'),
	url(r'^enviados/$', 'Nav.views.enviados'),


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
