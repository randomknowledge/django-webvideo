# coding: utf-8
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django_webvideo import constants
from django_webvideo.models import WebVideo, VideoScreen, ConvertedVideo
from django_webvideo.settings import get_setting
from django_webvideo.templatetags.webvideo_tags import video_tag
from django.utils.translation import ugettext_lazy as _
from django_webvideo.utils import sizeof_fmt, url_to_edit_object


preview_disclaimer = _("Video is embedded as {codec} only, which is eventually not supported by your webbrowser!")


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


def admin_thumb_helper_video(obj=True, for_admin=True, height=100, width=0):
    def admin_thumb(*args):
        obj = args[1 if for_admin else 0]
        vid = obj.original if isinstance(obj, ConvertedVideo) else obj

        screens = vid.screen.all()
        if len(screens) > 1:
            screen = screens[1]
        else:
            screen = screens[0]
        return '<a href="{url}"><img height="{height}" src="{src}" /></a>'.format(
            url=url_to_edit_object(obj),
            height=height,
            src=get_resized_image(screen.image, height=height, width=width)
        )
    admin_thumb.allow_tags = True
    admin_thumb.short_description = _('Preview')

    return admin_thumb


def admin_thumb_helper_videoscreen(image_object=True, for_admin=True, height=100, width=0):
    def admin_thumb(*args):
        obj = args[1 if for_admin else 0]
        return '<a href="{url}"><img height="{height}" src="{src}" /></a>'.format(
            url=url_to_edit_object(obj),
            height=height,
            width=width,
            src=get_resized_image(obj.image, height=height, width=width)
        )
    admin_thumb.allow_tags = True
    admin_thumb.short_description = _('Preview')

    return admin_thumb


def admin_video_helper(obj=True, for_admin=True):
    def admin_video(*args):
        obj = args[1 if for_admin else 0]
        if isinstance(obj, ConvertedVideo):
            return "{disclaimer}{video}".format(
                disclaimer=mark_safe(
                    "<p class='text-error'>{text}</p>".format(
                        text=preview_disclaimer.format(
                            codec="<strong>{0}</strong>".format(obj.codec)
                        )
                    )
                ),
                video=video_tag(obj.original, quality=obj.quality, preload='meta', width='100%', height='auto',
                                screen_num=2, codec=obj.codec)
            )
        else:
            return video_tag(obj, quality='max', preload='meta', width='100%', height='auto', screen_num=2)
    admin_video.allow_tags = True
    admin_video.short_description = _('Preview')
    return admin_video


def admin_filesize_helper(obj=True, for_admin=True):
    def admin_filesize(*args):
        obj = args[1 if for_admin else 0]
        return sizeof_fmt(obj.filesize)
    admin_filesize.short_description = _('Filesize')
    admin_filesize.admin_order_field = 'filesize'
    return admin_filesize


class ConvertedVideoInline(admin.StackedInline):
    model = ConvertedVideo
    extra = 0

    fields = ('video', 'admin_video', 'admin_filesize', 'codec', 'quality', 'width', 'height', 'bitrate', )
    readonly_fields = ('admin_video', 'admin_filesize', 'codec', 'quality', 'width', 'height', 'bitrate', )
    admin_video = admin_video_helper()
    admin_filesize = admin_filesize_helper()


class WebVideoForm(forms.ModelForm):
    target_codecs = forms.MultipleChoiceField(
        choices=constants.VIDEO_CODEC_CHOICES,
        initial=constants.VIDEO_CODECS.keys(),
        required=False,
    )
    target_qualities = forms.MultipleChoiceField(
        choices=constants.VIDEO_QUALITY_CHOICES,
        initial=constants.VIDEO_QUALITIES + ('original',),
        required=False,
    )

    class Meta:
        model = WebVideo


class OwnerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        obj.save()

    def queryset(self, request):
        return super(OwnerAdmin, self).queryset(request).filter(owner=request.user)


class VideoScreenAdmin(OwnerAdmin):
    list_display = ('video', 'admin_thumb_list', 'num', )
    list_display_links = ('video', 'num', )
    fields = ('video', 'image', 'admin_thumb', 'num', )
    readonly_fields = ('video', 'admin_thumb', 'num', )

    admin_thumb_list = admin_thumb_helper_videoscreen(width=200, height=80)
    admin_thumb = admin_thumb_helper_videoscreen(height=300)

    def has_add_permission(self, request):
        return False


class WebVideoAdmin(OwnerAdmin):
    list_display = (
        'video',
        'admin_thumb',
        'admin_filesize',
        'duration',
        'width',
        'height',
        'bitrate',
        'framerate',
    )
    list_display_links = (
        'video',
        'admin_filesize',
        'duration',
        'width',
        'height',
        'bitrate',
        'framerate',
    )
    edit_fields = (
        'video',
        'admin_video',
        'admin_filesize',
        'duration',
        'width',
        'height',
        'bitrate',
        'framerate',
        'converted_list_admin',
        'codecs',
        'qualities',
    )
    edit_readonly_fields = (
        'admin_video',
        'admin_filesize',
        'duration',
        'width',
        'height',
        'bitrate',
        'framerate',
        'converted_list_admin',
        'codecs',
        'qualities',
    )

    inlines = (ConvertedVideoInline, )

    admin_thumb = admin_thumb_helper_video(width=100, height=50)
    admin_video = admin_video_helper()
    admin_filesize = admin_filesize_helper()

    form = WebVideoForm

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing
            return self.edit_readonly_fields
        return ()#('admin_video', 'admin_filesize', 'converted_list_admin')
    
    def get_fieldsets(self, request, obj=None):
        if obj:  # Editing
            return [(None, {'fields': self.edit_fields})]
        return [(None, {'fields': ('video', 'target_codecs', 'target_qualities',)})]

    def get_inline_instances(self, request, obj=None):
        if obj:  # Editing
            return super(WebVideoAdmin, self).get_inline_instances(request, obj)
        return []

    def save_model(self, request, obj, form, change):
        print form.cleaned_data['target_codecs']
        print form.cleaned_data['target_qualities']
        obj.codecs = ','.join(form.cleaned_data['target_codecs'])
        obj.qualities = ','.join(form.cleaned_data['target_qualities'])
        #obj.codecs = 'Foo #%d' % form.cleaned_data['calculated']
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        obj.save()


class ConvertedVideoAdmin(OwnerAdmin):
    list_display = (
        'video',
        'admin_thumb',
        'original',
        'admin_filesize',
        'codec',
        'quality',
        'duration',
        'width',
        'height',
        'bitrate',
        'framerate',
    )
    list_display_links = (
        'video',
        'original',
        'admin_filesize',
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
        'admin_filesize',
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
        'admin_filesize',
        'codec',
        'quality',
        'duration',
        'width',
        'height',
        'bitrate',
        'framerate',
    )
    list_filter = ('codec', 'quality', )

    admin_thumb = admin_thumb_helper_video(width=50, height=30)
    admin_video = admin_video_helper()
    admin_filesize = admin_filesize_helper()

    def has_add_permission(self, request):
        return False


if get_setting('use_admin'):
    admin.site.register(WebVideo, WebVideoAdmin)
    admin.site.register(VideoScreen, VideoScreenAdmin)
    admin.site.register(ConvertedVideo, ConvertedVideoAdmin)
