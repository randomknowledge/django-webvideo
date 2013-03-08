# coding: utf-8
from django.core.management import BaseCommand
from django_webvideo import constants
from django_webvideo.models import WebVideo


class Command(BaseCommand):
    def handle(self, *args, **options):
        for video in WebVideo.objects.filter(status=constants.VIDEO_STATE_PENDING):
            video.convert()
