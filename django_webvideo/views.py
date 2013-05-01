# coding=utf-8
import tempfile
import zipfile
from django.db.models import Q
from easy_thumbnails.models import Source
import os
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseNotFound
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render, get_object_or_404
from django_webvideo.models import WebVideo, VideoScreen, ConvertedVideo
from sendfile import sendfile


def test(request):
    video = None
    videos = WebVideo.objects.all()
    if len(videos) > 0:
        video = videos[0]

    return render(
        request,
        'django_webvideo/test.html',
        {
            'video': video
        }
    )


def upload_test(request):
    return render(
        request,
        'django_webvideo/upload_test.html',
    )


def download(request, pk, codec, quality):
    if not request.user:
        return HttpResponseForbidden()
    user = request.user
    if not user.is_active or not user.is_authenticated() or not user.is_staff:
        return HttpResponseForbidden()

    video = get_object_or_404(WebVideo, pk=pk)
    if not user.is_superuser and video.owner != user:
        return HttpResponseForbidden()

    try:
        video = video.converted.filter(codec=codec, quality=quality)[0]
    except IndexError:
        return HttpResponseNotFound()

    filename = video.video.path
    basename, _ = os.path.splitext(os.path.basename(filename))
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    archive.write(filename, os.path.basename(filename))
    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename={0}.zip'.format(basename)
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response


def serve_media(request, path):
    if path.startswith("videos/"):
        if not request.user:
            return HttpResponseForbidden()
        user = request.user
        if not user.is_active or not user.is_authenticated() or not user.is_staff:
            return HttpResponseForbidden()

        if path.startswith("videos/screens/"):
            try:
                sources = Source.objects.filter(thumbnails__name=path).values_list("name")[0]
            except IndexError:
                sources = ()
            try:
                screen = VideoScreen.objects.get(Q(image__in=sources) | Q(image=path))
                if not user.is_superuser and screen.owner != user:
                    return HttpResponseForbidden()
            except VideoScreen.DoesNotExist:
                return HttpResponseNotFound()
        elif path.startswith("videos/converted/"):
            try:
                video = ConvertedVideo.objects.get(video=path)
                if not user.is_superuser and video.owner != user:
                    return HttpResponseForbidden()
            except ConvertedVideo.DoesNotExist:
                return HttpResponseNotFound()
        else:
            try:
                video = WebVideo.objects.get(video=path)
                if not user.is_superuser and video.owner != user:
                    return HttpResponseForbidden()
            except WebVideo.DoesNotExist:
                return HttpResponseNotFound()

    return sendfile(request, os.path.join(settings.MEDIA_ROOT, path))
