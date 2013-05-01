# coding=utf-8
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_webvideo.conf.prod")

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()