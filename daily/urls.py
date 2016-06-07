from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib.sitemaps import GenericSitemap
from content.models import Blog
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
from haystack.query import SearchQuerySet
from haystack.views import SearchView
from django.views.generic.base import RedirectView
#admin.autodiscover()


sqs = SearchQuerySet().order_by('-date')

blogs_dict = {
    'queryset': Blog.objects.all(),
    'date_field': 'date',
}

sitemaps = {
    # 'flatpages': FlatPageSitemap,
    'blogs': GenericSitemap(blogs_dict, priority=0.6),
}


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'daily.views.home', name='home'),
    url(r'^$', 'content.views.index'),
    url(r'^center/', 'content.views.center'),
    url(r'^mess/', 'content.views.mess'),
    url(r'^write/', 'content.views.publish'),
    url(r'^updatenickname/', 'content.views.updatenickname'),
    url(r'^updatehead/', 'content.views.updatehead'),
    url(r'^blog/(?P<bid>\d+)/', 'content.views.blog'),
    url(r'^deleteblog/(?P<bid>\d+)/', 'content.views.deleteblog'),
    url(r'^editblog/(?P<bid>\d+)/', 'content.views.editblog'),
     url(r'^login/', 'content.views.signin'),
    url(r'^signup/', 'content.views.signup'),
    url(r'^signout/', 'content.views.signout'),
    url(r'^protocol/', 'content.views.protocol'),
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
    #url(r'^favicon\.ico$',RedirectView.as_view(url='/assets/source/favicon.ico')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    )


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('', (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))

