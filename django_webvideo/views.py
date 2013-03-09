# coding=utf-8
from django.shortcuts import render
from django_webvideo.models import WebVideo


def test(request):
    video = None
    videos = WebVideo.objects.all()
    if len(videos) > 1:
        video = videos[1]

    return render(
        request,
        'django_webvideo/test.html',
        {
            'video': video
        }
    )