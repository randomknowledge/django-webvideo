# coding=utf-8
from django.conf import settings
from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    url(r'^test/?$', 'django_webvideo.views.test', name='test')
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    )
