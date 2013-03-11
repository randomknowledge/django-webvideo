# coding: utf-8
from django.contrib import admin
from django_webvideo.models import WebVideo, VideoScreen, ConvertedVideo
from django_webvideo.settings import get_setting
from django_webvideo.templatetags.webvideo_tags import video_tag
from django.utils.translation import ugettext_lazy as _
from django_webvideo.utils import filesize_human_readable


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
    admin_thumb.short_description = _('Preview')

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
    admin_thumb.short_description = _('Preview')

    return admin_thumb


def admin_video_helper(obj=True, for_admin=True):
    def admin_video(*args):
        obj = args[1 if for_admin else 0]
        if isinstance(obj, ConvertedVideo):
            return video_tag(obj.original, quality=obj.quality, preload='meta', width='100%', height='auto',
                             screen_num=2)
        else:
            return video_tag(obj, quality='max', preload='meta', width='100%', height='auto', screen_num=2)
    admin_video.allow_tags = True
    admin_video.short_description = _('Preview')
    return admin_video


def admin_filesize_helper(obj=True, for_admin=True):
    def admin_filesize(*args):
        obj = args[1 if for_admin else 0]
        if isinstance(obj, ConvertedVideo):
            return filesize_human_readable(obj.video.path)
        else:
            return filesize_human_readable(obj.video.path)
    admin_filesize.short_description = _('Filesize')
    return admin_filesize


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
    admin_thumb.short_description = _('Preview')

    return admin_thumb


class ConvertedVideoInline(admin.StackedInline):
    model = ConvertedVideo
    extra = 0

    fields = ('video', 'admin_video', 'filezize', 'codec', 'quality', 'width', 'height', 'bitrate', )
    readonly_fields = ('admin_video', 'filezize', 'codec', 'quality', 'width', 'height', 'bitrate', )
    admin_video = admin_video_helper()
    filezize = admin_filesize_helper()


class VideoScreenAdmin(admin.ModelAdmin):
    list_display = ('video', 'admin_thumb', 'num', )
    fields = ('video', 'image', 'admin_thumb', 'num', )
    readonly_fields = ('video', 'admin_thumb', 'num', )

    admin_thumb = admin_thumb_helper_videoscreen()


class WebVideoAdmin(admin.ModelAdmin):
    list_display = (
        'video',
        'admin_thumb',
        'filezize',
        'duration',
        'width',
        'height',
        'bitrate',
        'framerate',
    )
    fields = (
        'video',
        'admin_video',
        'filezize',
        'duration',
        'width',
        'height',
        'bitrate',
        'framerate',
        'converted_list_admin',
    )
    readonly_fields = (
        'admin_video',
        'filezize',
        'duration',
        'width',
        'height',
        'bitrate',
        'framerate',
        'converted_list_admin',
    )
    inlines = (ConvertedVideoInline, )

    admin_thumb = admin_thumb_helper_webvideo()
    admin_video = admin_video_helper()
    filezize = admin_filesize_helper()


class ConvertedVideoAdmin(admin.ModelAdmin):
    list_display = (
        'video',
        'admin_thumb',
        'original',
        'filezize',
        'codec',
        'quality',
        'duration',
        'width',
        'height',
        'bitrate',
        'framerate',
    )
    fields = (
        'video',
        'admin_video',
        'original',
        'filezize',
        'codec',
        'quality',
        'duration',
        'width',
        'height',
        'bitrate',
        'framerate',
    )
    readonly_fields = (
        'admin_video',
        'original',
        'filezize',
        'codec',
        'quality',
        'duration',
        'width',
        'height',
        'bitrate',
        'framerate',
    )
    list_filter = ('codec', 'quality', )

    admin_thumb = admin_thumb_helper_convertedvideo()
    admin_video = admin_video_helper()
    filezize = admin_filesize_helper()


if get_setting('use_admin'):
    admin.site.register(WebVideo, WebVideoAdmin)
    admin.site.register(VideoScreen, VideoScreenAdmin)
    admin.site.register(ConvertedVideo, ConvertedVideoAdmin)
