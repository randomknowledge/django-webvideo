# coding: utf-8
from django.template import Library, Context
from django.template.loader import render_to_string
from django_webvideo import constants


register = Library()


@register.simple_tag
def video_tag(video, quality='max', width=None, height=None, preload="auto", autoplay=False, controls=True,
              attributes="", screen_num=1):
    screen = video.get_screen(screen_num)

    converted = video.converted.all()
    if quality == 'max':
        for q in constants.VIDEO_QUALITIES:
            if converted.filter(quality=q).count() > 0:
                quality = q
                break

    converted = converted.filter(quality=quality)
    if len(converted) > 0:
        if width is None:
            width = converted[0].width
        if height is None:
            height = converted[0].height

    files = []
    for conv in converted:
        files.append({
            'obj': conv.video,
            'mime': constants.VIDEO_MIMETYPES.get(conv.codec)
        })

    return render_to_string("django_webvideo/snippets/video-embed.html", context_instance=Context({
        'video': video,
        'files': files,
        'width': width,
        'height': height,
        'preload': preload,
        'attributes': attributes,
        'autoplay': autoplay,
        'controls': controls,
        'poster': screen.image.url,
    }))
