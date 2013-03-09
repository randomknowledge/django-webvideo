# coding=utf-8
import re
import subprocess
from django.conf import settings
from django_webvideo.video import convert_video, video_info, create_screen_image, video_metadata
import os
from django.db import models
from django_webvideo.settings import get_setting
from django_webvideo import constants, queue
from django.utils.translation import ugettext_lazy as _


def _get_video_paths(infile, codec):
    if not codec in constants.VIDEO_CODECS.keys():
        raise AttributeError("Parameter 'codec' must be in {0}!".format(constants.VIDEO_CODECS.keys))
    ext = constants.VIDEO_CODECS.get(codec)

    basename, _ = os.path.splitext(os.path.basename(infile))
    paths = {}
    for quality in constants.VIDEO_QUALITIES + ('original',):
        rel = os.path.join(
            get_setting('convert_to'),
            "{0}.{1}.{2}.{3}".format(basename, codec, quality, ext)
        )
        paths[quality] = {
            'relative': rel,
            'absolute': os.path.join(
                settings.MEDIA_ROOT,
                rel,
            ),
        }
    return paths


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


def _convert_single(web_video, codec, quality):
    web_video._convert_single(codec, quality)


def _set_meta(video_obj, save=False):
    meta = video_metadata(video_obj.video.path)
    video_obj.duration = meta.get('duration')
    video_obj.width = meta.get('width')
    video_obj.height = meta.get('height')
    video_obj.bitrate = meta.get('bitrate')
    video_obj.framerate = meta.get('framerate')
    if save:
        video_obj.save()


class VideoScreen(models.Model):
    video = models.ForeignKey('WebVideo', related_name='screen')
    image = models.ImageField(upload_to=get_setting('screens_to'))
    num = models.IntegerField(max_length=2)

    class Meta:
        unique_together = ('video', 'num', )

    def __unicode__(self):
        return "{0}, Screen {1}".format(self.video.video, self.num)


class ConvertedVideo(models.Model):
    video = models.FileField(upload_to=get_setting('convert_to'))
    original = models.ForeignKey('WebVideo', related_name='converted')
    codec = models.CharField(max_length=20, choices=constants.VIDEO_CODEC_CHOICES)
    quality = models.CharField(max_length=20, choices=constants.VIDEO_QUALITY_CHOICES)
    duration = models.FloatField(default=0.0, verbose_name=_(u"Duration in seconds"))
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    bitrate = models.FloatField(default=0.0, verbose_name=_(u"Bitrate in kb/s"))
    framerate = models.FloatField(default=29.92)

    status = models.SmallIntegerField(
        choices=constants.VIDEO_STATE_CHOICES, default=constants.VIDEO_STATE_PENDING, editable=False
    )

    class Meta:
        unique_together = ('original', 'codec', 'quality', )

    def __unicode__(self):
        return "{0} ({1}, {2})".format(self.video, self.codec, self.quality)


class WebVideo(models.Model):
    video = models.FileField(upload_to=get_setting('upload_to'))
    duration = models.FloatField(default=0.0, verbose_name=_(u"Duration in seconds"))
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    bitrate = models.FloatField(default=0.0, verbose_name=_(u"Bitrate in kb/s"))
    framerate = models.FloatField(default=29.92)

    @property
    def status(self):
        if self.converted.all().count() == 0:
            return constants.VIDEO_STATE_PENDING
        else:
            return constants.VIDEO_STATE_SUCCESS

    def __unicode__(self):
        return self.video.url

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        old_video = None
        if self.pk is not None:
            try:
                old_video = WebVideo.objects.get(pk=self.pk).video
            except WebVideo.DoesNotExist:
                pass
        if old_video != self.video:
            self.converted.all().delete()
            self.screen.all().delete()
            super(WebVideo, self).save(force_insert, force_update, using, update_fields)
            _set_meta(self)
            self.create_screen_images()
            self.convert()
        super(WebVideo, self).save(force_insert, force_update, using, update_fields)

    def get_screen(self, num=1):
        try:
            return self.screen.get(video=self, num=num)
        except VideoScreen.DoesNotExist:
            return None

    def get_video(self, codec, quality):
        try:
            return self.converted.get(original=self, codec=codec, quality=quality)
        except ConvertedVideo.DoesNotExist:
            return None

    def convert(self):
        if self.status != constants.VIDEO_STATE_PENDING:
            return
        for codec in constants.VIDEO_CODECS.keys():
            for quality in constants.VIDEO_QUALITIES:
                minrate = constants.VIDEO_QUALITY_MIN_BITRATES[quality]
                if self.bitrate > 0 and self.bitrate >= minrate:
                    queue.enqueue(_convert_single, self, codec, quality)
            queue.enqueue(_convert_single, self, codec, 'original')

    def _convert_single(self, codec, quality):
        paths = _get_video_paths(self.video.path, codec)[quality]

        conv = ConvertedVideo(original=self, codec=codec, quality=quality)

        if convert_video(self.video.path, paths.get('absolute'), codec, quality, self.bitrate, self.width, self.height):
            # get object from db to prevent "no-save" bug in rq
            conv.video.name = paths.get('relative')
            conv.status = constants.VIDEO_STATE_SUCCESS
            _set_meta(conv)
            conv.save()
            return True
        else:
            conv.status = constants.VIDEO_STATE_ERROR
            conv.save()
            return False

    def create_screen_images(self):
        if self.duration == 0:
            return

        dur = self.duration

        for num in range(1, constants.NUM_SCREENS + 1):
            relative, absolute = _get_image_paths(self.video.path, num)
            if num == 1:
                frame = round(min(dur * 0.5, 0.5), 2)
            else:
                frame = round(dur / constants.NUM_SCREENS * (num * 0.9), 2)
            if create_screen_image(self.video.path, absolute, frame):
                VideoScreen(video=self, image=relative, num=num).save()

    def converted_list_admin(self):
        return ["{0}, {1}".format(c.codec, c.quality) for c in self.converted.all()]
    converted_list_admin.short_description = _('Variants')