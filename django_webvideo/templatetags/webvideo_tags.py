# coding: utf-8
from django.template import Library


register = Library()

@register.simple_tag
def video_tag(request, video, screen_number):
    return video
