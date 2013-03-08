# coding=utf-8
import os
from .base import *

DEBUG = True
THUMBNAIL_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'database.db'),
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
SOUTH_TESTS_MIGRATE = False
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(process)s] [%(levelname)s] %(name)s: %(message)s',
        },
        'simple': {
            'format': '>>> %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.db': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        'requests': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

try:
    from debug_toolbar import VERSION
except ImportError:
    pass
else:
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE_CLASSES += ("debug_toolbar.middleware.DebugToolbarMiddleware",)
