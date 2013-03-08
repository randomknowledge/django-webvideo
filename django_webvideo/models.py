# coding=utf-8
from django.conf import settings
from django_webvideo.video import convert_video
import os
from django.db import models
from django_webvideo.settings import get_setting
from django_webvideo import constants


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


class WebVideo(models.Model):
    original = models.FileField(upload_to=get_setting('upload_to'))
    h264 = models.FileField(upload_to=get_setting('convert_to'), blank=True, null=True, editable=False)
    oggvorbis = models.FileField(upload_to=get_setting('convert_to'), blank=True, null=True, editable=False)
    status = models.SmallIntegerField(
        choices=constants.VIDEO_STATE_CHOICES, default=constants.VIDEO_STATE_PENDING, editable=False
    )

    def convert(self):
        if self.status != constants.VIDEO_STATE_PENDING:
            return
        self.status = constants.VIDEO_STATE_INPROGRESS
        self.save()
        out1_rel, out1 = _get_video_paths(self.original.path, 'h264')
        out2_rel, out2 = _get_video_paths(self.original.path, 'ogv')
        result1 = convert_video(self.original.path, out1, 'h264')
        result2 = convert_video(self.original.path, out2, 'ogv')
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
