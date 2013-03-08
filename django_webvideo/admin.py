# coding: utf-8
from django.contrib import admin
from django_webvideo.models import WebVideo


class WebVideoAdmin(admin.ModelAdmin):
    list_display = ('original', 'status', )
    fields = ('status', 'original', 'h264', 'oggvorbis', )
    readonly_fields = ('status', 'h264', 'oggvorbis', )

admin.site.register(WebVideo, WebVideoAdmin)
