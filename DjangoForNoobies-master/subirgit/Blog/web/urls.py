from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
)

urlpatterns = patterns('appblog.views',
	(r"^entrada/ (?P<pk>\d+)$","entrada"),
	(r"^month/ (\d+)/(\d+)/$", "month"),
	(r"^poncomentario/(\d+)/$", "poncomentario"),
	(r'^admin/', include(admin.site.urls)),
	(r"", "main"),
)
