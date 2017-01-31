from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pw.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r"^entrada/ (?P<pk>\d+)$","trueque.views.entrada"),
		url(r"^month/ (\d+)/(\d+)/$", "trueque.views.month"),
		url(r"^poncomentario/(\d+)/$", "trueque.views.poncomentario"),
		url(r"^ponentrada/$", "trueque.views.ponentrada"),
		url(r"^registrar/$", "trueque.views.signup", name='signup'),
		url(r'^login$', login, {'template_name': 'login.html', }, name="login"),
		url(r'^home$', 'trueque.views.home', name='home'),
		url(r'^logout$', logout, {'template_name': 'estructura.html', }, name="logout"),
		url(r'^admin/', include(admin.site.urls)),
		url(r"", "trueque.views.main"),

)
