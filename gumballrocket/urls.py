from django.conf.urls import patterns, include, url

# enable the admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('api.views',
    url(r'^$', 'home'),

    # admin
    url(r'^admin/', include(admin.site.urls)),
)
