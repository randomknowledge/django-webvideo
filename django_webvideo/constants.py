# coding: utf-8
from django.utils.translation import ugettext_lazy as _

VIDEO_STATE_PENDING = 0
VIDEO_STATE_INPROGRESS = 1
VIDEO_STATE_ERROR = 2
VIDEO_STATE_SUCCESS = 3

VIDEO_QUALITY_HIGH = 'high'
VIDEO_QUALITY_SEMIHIGH = 'semi-high'
VIDEO_QUALITY_MEDIUM = 'medium'
VIDEO_QUALITY_LOW = 'low'

VIDEO_STATES = {
    VIDEO_STATE_PENDING: _(u'pending'),
    VIDEO_STATE_INPROGRESS: _(u'in progress'),
    VIDEO_STATE_ERROR: _(u'error'),
    VIDEO_STATE_SUCCESS: _(u'ready'),
}

VIDEO_STATE_CHOICES = ()
for key, value in VIDEO_STATES.iteritems():
    VIDEO_STATE_CHOICES += ((key, value),)

VIDEO_CODECS = {
    'h264': 'mp4',
    'ogv': 'ogv',
    'webm': 'webm',
}

NUM_SCREENS = 3

VIDEO_QUALITIES = (VIDEO_QUALITY_HIGH, VIDEO_QUALITY_SEMIHIGH, VIDEO_QUALITY_MEDIUM, VIDEO_QUALITY_LOW, )

VIDEO_QUALITY_MIN_BITRATES = {
    VIDEO_QUALITY_HIGH: 1001,
    VIDEO_QUALITY_SEMIHIGH: 501,
    VIDEO_QUALITY_MEDIUM: 301,
    VIDEO_QUALITY_LOW: 0,
}

VIDEO_MIMETYPES = {
    'h264': 'video/mp4; codecs="avc1.4D401E, mp4a.40.2"',
    'ogv': 'video/ogg; codecs="theora, vorbis"',
    'webm': 'video/webm; codecs="vp8.0, vorbis"',
}

VIDEO_SIZES = {
    VIDEO_QUALITY_HIGH: (1920, 1080,),
    VIDEO_QUALITY_SEMIHIGH: (1280, 720,),
    VIDEO_QUALITY_MEDIUM: (854, 480,),
    VIDEO_QUALITY_LOW: (640, 360,),
}

VIDEO_CODEC_CHOICES = ()
for key in VIDEO_CODECS.keys():
    VIDEO_CODEC_CHOICES += ((key, key),)

VIDEO_QUALITY_CHOICES = ()
for key in VIDEO_QUALITIES:
    VIDEO_QUALITY_CHOICES += ((key, key),)
VIDEO_QUALITY_CHOICES += (('original', 'original'),)