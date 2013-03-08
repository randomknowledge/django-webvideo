# coding=utf-8
import re
from django.conf import settings
from django_webvideo.video import convert_video, video_info, create_screen_image
import os
from django.db import models
from django_webvideo.settings import get_setting
from django_webvideo import constants
from django.utils.translation import ugettext_lazy as _


def _get_video_paths(infile, codec):
    if not codec in ('h264', 'ogv'):
        raise AttributeError("Parameter 'codec' must be either 'h264' or 'ogv'!")
    ext = 'mp4' if codec == 'h264' else 'ogv'

    basename, _ = os.path.splitext(os.path.basename(infile))
    path_rel = os.path.join(
        get_setting('convert_to'),
        "{0}.{1}.{2}".format(basename, codec, ext)
    )

    path_abs = os.path.join(
        settings.MEDIA_ROOT,
        path_rel,
    )

    return path_rel, path_abs


def _get_image_paths(infile, n):
    basename, _ = os.path.splitext(os.path.basename(infile))
    path_rel = os.path.join(
        get_setting('screens_to'),
        "{0}.{1}.jpg".format(basename, n)
    )

    path_abs = os.path.join(
        settings.MEDIA_ROOT,
        path_rel,
    )

    return path_rel, path_abs


class WebVideo(models.Model):
    original = models.FileField(upload_to=get_setting('upload_to'))
    h264 = models.FileField(upload_to=get_setting('convert_to'), blank=True, null=True, editable=False)
    oggvorbis = models.FileField(upload_to=get_setting('convert_to'), blank=True, null=True, editable=False)
    status = models.SmallIntegerField(
        choices=constants.VIDEO_STATE_CHOICES, default=constants.VIDEO_STATE_PENDING, editable=False
    )
    duration = models.FloatField(default=0.0, verbose_name=_(u"Duration in seconds"))
    screen_1 = models.ImageField(upload_to=get_setting('screens_to'), blank=True, null=True)
    screen_2 = models.ImageField(upload_to=get_setting('screens_to'), blank=True, null=True)
    screen_3 = models.ImageField(upload_to=get_setting('screens_to'), blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        old_video = None
        if self.pk is not None:
            try:
                old_video = WebVideo.objects.get(pk=self.pk).original
            except WebVideo.DoesNotExist:
                pass
        if old_video != self.original:
            super(WebVideo, self).save(force_insert, force_update, using, update_fields)
            self.duration = self._get_calculated_duration()
            self.create_screen_images()
            # TODO: enqueue video conversion
        super(WebVideo, self).save(force_insert, force_update, using, update_fields)

    def _get_calculated_duration(self):
        info = video_info(self.original.path)
        if not info:
            return 0.0
        m = re.search(r'Duration: (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>[\d\.]+)', info)

        if m:
            return float(m.group('hours')) * 3600 + float(m.group('minutes')) * 60 + float(m.group('seconds'))
        return 0.0

    def get_screen(self, num=1):
        return getattr(self, 'screen_{0}'.format(num))

    def convert(self):
        if self.status != constants.VIDEO_STATE_PENDING:
            return
        self.status = constants.VIDEO_STATE_INPROGRESS
        self.save()
        out1_rel, out1_abs = _get_video_paths(self.original.path, 'h264')
        out2_rel, out2_abs = _get_video_paths(self.original.path, 'ogv')
        result1 = convert_video(self.original.path, out1_abs, 'h264')
        result2 = convert_video(self.original.path, out2_abs, 'ogv')
        if result1 and result2:
            self.h264.name = out1_rel
            self.oggvorbis.name = out2_rel
            self.status = constants.VIDEO_STATE_SUCCESS
        else:
            if result1:
                self.h264.name = out1_rel
            if result2:
                self.oggvorbis.name = out2_rel
            self.status = constants.VIDEO_STATE_ERROR
        self.save()

    def create_screen_images(self):
        if self.duration == 0:
            return
        out1_rel, out1_abs = _get_image_paths(self.original.path, 1)
        out2_rel, out2_abs = _get_image_paths(self.original.path, 2)
        out3_rel, out3_abs = _get_image_paths(self.original.path, 3)

        dur = self.duration
        first_frame = round(min(dur * 0.5, 0.5), 2)
        second_frame = round(dur * 0.3, 2)
        third_frame = round(dur * 0.7, 2)

        if create_screen_image(self.original.path, out1_abs, first_frame):
            self.screen_1.name = out1_rel
        if create_screen_image(self.original.path, out2_abs, second_frame):
            self.screen_2.name = out2_rel
        if create_screen_image(self.original.path, out3_abs, third_frame):
            self.screen_3.name = out3_rel

    def get_resized_screen(self, screen=1, width=0, height=0, upscale=True):
        from easy_thumbnails.files import get_thumbnailer
        from easy_thumbnails.exceptions import InvalidImageFormatError

        options = {
            'size': (width, height),
            'upscale': upscale,
            'crop': width and height,
        }
        img = self.get_screen(screen)
        if img:
            try:
                return get_thumbnailer(img).get_thumbnail(options).url
            except (InvalidImageFormatError, IOError):
                pass

        return self.image.url
