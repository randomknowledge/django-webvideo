# coding: utf-8
from django.contrib import admin
from django_webvideo.models import WebVideo, VideoScreen, ConvertedVideo
from django_webvideo.settings import get_setting


def get_resized_image(image, width=0, height=0, upscale=True):
    from easy_thumbnails.files import get_thumbnailer
    from easy_thumbnails.exceptions import InvalidImageFormatError

    options = {
        'size': (width, height),
        'upscale': upscale,
        'crop': width and height,
        }
    try:
        return get_thumbnailer(image).get_thumbnail(options).url
    except (InvalidImageFormatError, IOError):
        pass

    return image.url


def admin_thumb_helper_webvideo(image_object=True, for_admin=True, height=100, width=0):
    def admin_thumb(*args):
        obj = args[1 if for_admin else 0]

        s = ""
        try:
            screens = obj.screen.all()
            if len(screens) > 1:
                screen = screens[1]
            else:
                screen = screens[0]
            s = "%s" % ('<a href="%s" target="_blank"><img height="%s" src="%s" /></a>' % (
                screen.image.url, height, get_resized_image(screen.image, height=height, width=width)))
        except Exception:
            pass

        return s
    admin_thumb.allow_tags = True
    admin_thumb.short_description = 'Vorschau'

    return admin_thumb


def admin_thumb_helper_videoscreen(image_object=True, for_admin=True, height=100, width=0):
    def admin_thumb(*args):
        obj = args[1 if for_admin else 0]

        s = ""
        i = 1
        try:
            s = "%s" % ('<a href="%s" target="_blank"><img height="%s" src="%s" /></a>' % (
                obj.image.url, height, get_resized_image(obj.image, height=height, width=width)))
        except ValueError:
            pass
        i += 1

        return s
    admin_thumb.allow_tags = True
    admin_thumb.short_description = 'Vorschau'

    return admin_thumb


def admin_thumb_helper_convertedvideo(image_object=True, for_admin=True, height=50, width=0):
    def admin_thumb(*args):
        obj = args[1 if for_admin else 0]

        s = ""
        try:
            screens = obj.original.screen.all()
            if len(screens) > 1:
                screen = screens[1]
            else:
                screen = screens[0]
            s = "%s" % ('<a href="%s" target="_blank"><img height="%s" src="%s" /></a>' % (
                screen.image.url, height, get_resized_image(screen.image, height=height, width=width)))
        except Exception:
            pass

        return s
    admin_thumb.allow_tags = True
    admin_thumb.short_description = 'Vorschau'

    return admin_thumb


class VideoScreenAdmin(admin.ModelAdmin):
    list_display = ('video', 'admin_thumb', 'num', )
    fields = ('video', 'image', 'admin_thumb', 'num', )
    readonly_fields = ('video', 'admin_thumb', 'num', )

    admin_thumb = admin_thumb_helper_videoscreen()


class WebVideoAdmin(admin.ModelAdmin):
    list_display = ('video', 'admin_thumb', 'duration', 'width', 'height', 'bitrate', 'framerate', )
    fields = ('video', 'admin_thumb', 'duration', 'width', 'height', 'bitrate', 'framerate', 'converted_list_admin', )
    readonly_fields = ('admin_thumb', 'duration', 'width', 'height', 'bitrate', 'framerate', 'converted_list_admin', )

    admin_thumb = admin_thumb_helper_webvideo()


class ConvertedVideoAdmin(admin.ModelAdmin):
    list_display = ('video', 'admin_thumb', 'original', 'codec', 'quality', 'duration', 'width', 'height', 'bitrate', 'framerate', )
    fields = ('video', 'admin_thumb', 'original', 'codec', 'quality', 'duration', 'width', 'height', 'bitrate', 'framerate', )
    readonly_fields = ('admin_thumb', 'original', 'codec', 'quality', 'duration', 'width', 'height', 'bitrate', 'framerate', )
    list_filter = ('codec', 'quality', )

    admin_thumb = admin_thumb_helper_convertedvideo()


if get_setting('use_admin'):
    admin.site.register(WebVideo, WebVideoAdmin)
    admin.site.register(VideoScreen, VideoScreenAdmin)
    admin.site.register(ConvertedVideo, ConvertedVideoAdmin)
