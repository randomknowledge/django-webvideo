# coding=utf-8
from django_webvideo.conf.dev import *

try:
    from settings_local import *
except ImportError:
    pass
