# coding=utf-8
from tastypie.cache import SimpleCache
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.serializers import Serializer
from tastypie.throttle import CacheThrottle
from django_webvideo.models import WebVideo, ConvertedVideo


class WebVideoAuthorization(DjangoAuthorization):
    pass


class WebVideoAuthentication(SessionAuthentication):
    def is_authenticated(self, request, **kwargs):
        if request.META.has_key('CSRF_COOKIE') and not request.META.has_key('HTTP_X_CSRFTOKEN'):
            request.META["HTTP_X_CSRFTOKEN"] = request.META.get('CSRF_COOKIE', '')
        return super(WebVideoAuthentication, self).is_authenticated(request, **kwargs)


class MultipartResource(object):
    def deserialize(self, request, data, format=None):
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')
        if format == 'application/x-www-form-urlencoded':
            return request.POST
        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(MultipartResource, self).deserialize(request, data, format)

    def put_detail(self, request, **kwargs):
        if not hasattr(request, '_body'):
            request._body = ''
        return super(MultipartResource, self).put_detail(request, **kwargs)


class ConvertedVideoResource(ModelResource):
    class Meta:
        queryset = ConvertedVideo.objects.all()
        resource_name = 'converted'
        excludes = ['status', ]


class WebVideoResource(MultipartResource, ModelResource):
    video = fields.FileField(attribute="video")
    versions = fields.OneToManyField(ConvertedVideoResource, 'converted', full=True, null=True, blank=True)

    class Meta:
        queryset = WebVideo.objects.all()
        resource_name = 'video'
        fields = ['id', 'versions', 'duration', 'video', ]
        allowed_methods = ['get', 'post', ]

        filtering = {
            'duration': ['exact', 'gt', 'gte', 'lt', 'lte', 'range'],
        }

        authentication = WebVideoAuthentication()
        authorization = WebVideoAuthorization()
        cache = SimpleCache(timeout=300)
        throttle = CacheThrottle(throttle_at=50, timeframe=60)
        serializer = Serializer(formats=['json', ])
