# coding=utf-8
from django.shortcuts import render
from django_webvideo.models import WebVideo


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