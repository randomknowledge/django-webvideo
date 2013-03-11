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
    (r'^api/', include(v1_api.urls)),
)

if 'django_webvideo.queueadmin' in settings.INSTALLED_APPS:
    urlpatterns = patterns(
        '',
        url(
            r'^queueadmin/',
            include('django_webvideo.queueadmin.urls', namespace='queueadmin', app_name='queueadmin')
        ),
    )

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    )
