# coding: utf-8
from django.template import Library, Context
from django.template.loader import render_to_string


register = Library()


@register.simple_tag
def video_tag(video, width=None, height=None, preload="auto", autoplay=False, controls=True, attributes="", screen_num=1):
    screen = video.get_screen(screen_num)
    if width is None:
        width = screen.width
    if height is None:
        height = screen.height

    return render_to_string("django_webvideo/snippets/video-embed.html", context_instance=Context({
        'video': video,
        'width': width,
        'height': height,
        'preload': preload,
        'attributes': attributes,
        'autoplay': autoplay,
        'controls': controls,
        'poster': screen.url,
    }))
