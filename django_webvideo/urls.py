# coding=utf-8
from django.conf import settings
from django.conf.urls import patterns, url, include
from tastypie.api import Api
from django_webvideo.api import WebVideoResource

v1_api = Api(api_name='v1')
v1_api.register(WebVideoResource())


urlpatterns = patterns(
    '',
    url(r'^test/?$', 'django_webvideo.views.test', name='test'),
    url(r'^upload_test/?$', 'django_webvideo.views.upload_test', name='upload_test'),
    url(r'download/(?P<pk>\d+)/(?P<codec>[a-z0-9_-]+)/(?P<quality>[a-z0-9_-]+)/?$', 'django_webvideo.views.download', name='download'),
    (r'^api/', include(v1_api.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    )
elif "sendfile" in settings.INSTALLED_APPS:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django_webvideo.views.serve_media'),
    )
