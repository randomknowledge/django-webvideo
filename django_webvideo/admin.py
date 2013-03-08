# coding: utf-8
from django.contrib import admin
from django_webvideo.models import WebVideo
from django_webvideo.settings import get_setting


def admin_thumb_helper(image_object=True, for_admin=True, height=100, width=0):
    def admin_thumb(*args):
        obj = args[1 if for_admin else 0]

        s = ""
        i = 1
        for img in (obj.screen_1, obj.screen_2, obj.screen_3):
            try:
                s = "%s%s" % (s, '<a href="%s" target="_blank"><img height="%s" src="%s" /></a>' % (
                    img.url, height, obj.get_resized_screen(i, height=height, width=width)))
            except ValueError:
                pass
            i += 1

        return s
    admin_thumb.allow_tags = True
    admin_thumb.short_description = 'Vorschau'

    return admin_thumb


class WebVideoAdmin(admin.ModelAdmin):
    list_display = ('original', 'status', 'duration', 'admin_thumb', )
    fields = ('status', 'original', 'h264', 'oggtheora', 'duration', 'screen_1', 'screen_2', 'screen_3', )
    readonly_fields = ('status', 'h264', 'oggtheora', 'duration', )

    admin_thumb = admin_thumb_helper()


if get_setting('use_admin'):
    admin.site.register(WebVideo, WebVideoAdmin)
