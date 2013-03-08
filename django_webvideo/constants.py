# coding: utf-8
from django.utils.translation import ugettext_lazy as _

VIDEO_STATE_PENDING = 0
VIDEO_STATE_INPROGRESS = 1
VIDEO_STATE_ERROR = 2
VIDEO_STATE_SUCCESS = 3

VIDEO_STATES = {
    VIDEO_STATE_PENDING: _(u'pending'),
    VIDEO_STATE_INPROGRESS: _(u'in progress'),
    VIDEO_STATE_ERROR: _(u'error'),
    VIDEO_STATE_SUCCESS: _(u'ready'),
}

VIDEO_STATE_CHOICES = ()
for key, value in VIDEO_STATES.iteritems():
    VIDEO_STATE_CHOICES += ((key, value),)
