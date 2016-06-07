from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib.sitemaps import GenericSitemap

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
#from haystack.query import SearchQuerySet
from haystack.views import SearchView
from django.views.generic.base import RedirectView
#admin.autodiscover()







urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'daily.views.home', name='home'),
    #url(r'^favicon\.ico$',RedirectView.as_view(url='/assets/source/favicon.ico')),
    url(r'^admin/', include(admin.site.urls)),
    )


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('', (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))

