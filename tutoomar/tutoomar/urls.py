from django.conf.urls import patterns, include, url
from django.contrib import admin
from blog import views as blog_vistas

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tutoomar.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', blog_vistas.index),
    url(r'^login/', blog_vistas.login_view),
    url(r'^register/', blog_vistas.register_view),
    url(r'^logout/', blog_vistas.logout_view),
    url(r'^publicar/',blog_vistas.publicar_view),
    url(r'^articulosprivados/', blog_vistas.articulosprivados_view),
    url(r'^articulo/(?P<num>[0-9]+)/',blog_vistas.modificar_view),
    url(r'^borrar/(?P<num>[0-9]+)/', blog_vistas.borrar_view),
)
