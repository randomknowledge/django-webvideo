# coding=utf-8
import os
from math import log
from django.core.urlresolvers import reverse

unit_list = zip(['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'], [0, 0, 1, 2, 2, 2])


def sizeof_fmt(num):
    """Human friendly file size"""
    if num > 1:
        exponent = min(int(log(num, 1024)), len(unit_list) - 1)
        quotient = float(num) / 1024**exponent
        unit, num_decimals = unit_list[exponent]
        format_string = '{:.%sf} {}' % (num_decimals)
        return format_string.format(quotient, unit)
    if num == 0:
        return '0 bytes'
    if num == 1:
        return '1 byte'


def filesize_human_readable(path):
    return sizeof_fmt(os.stat(path).st_size)


def url_to_edit_object(obj):
    return reverse('admin:{0}_{1}_change'.format(obj._meta.app_label,  obj._meta.module_name),  args=[obj.id], )