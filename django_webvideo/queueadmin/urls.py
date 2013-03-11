# coding=utf-8
from django.conf.urls import patterns, url
from tastypie.api import Api
from django_webvideo.api import WebVideoResource

v1_api = Api(api_name='v1')
v1_api.register(WebVideoResource())


urlpatterns = patterns(
    '',
    url(r'^/?$', 'django_webvideo.queueadmin.views.index', name='index'),
    url(r'^login/?$', 'django_webvideo.queueadmin.views.login', name='login'),
    url(r'^logout/?$', 'django_webvideo.queueadmin.views.logout', name='logout'),
)
