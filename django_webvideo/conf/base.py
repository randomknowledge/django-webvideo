# coding=utf-8
import os
import platform

_ = lambda s: s


PROJECT_NAME = 'django_webvideo'
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        os.pardir,
    )
)

PROJECT_DIR = os.path.abspath(
    os.path.join(
        BASE_DIR, PROJECT_NAME
    )
)

# Workaround for bug in Pycharm when calling syncdb on mac
if platform.system() == 'Darwin':
    os.environ['LANG'] = 'de_DE.UTF-8'

TEMPLATE_DEBUG = True
TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'de'
SITE_ID = 1

LANGUAGES = (
    ('de', _('German')),
)

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

USE_I18N = True
USE_L10N = True
USE_TZ = True

EMAIL_SUBJECT_PREFIX = '[%s] ' % PROJECT_NAME

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'z6u-wc2gat@l_o4cpq931+b*&5g7i*r-031ar&1d&534-e3w#d'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

MIDDLEWARE_CLASSES = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',

    'easy_thumbnails',
    'django_webvideo',
]

TEMPLATE_DIRS = (
    '%s/templates' % PROJECT_DIR,
)
STATICFILES_DIRS = (
    '%s/static' % BASE_DIR,
)
LOCALE_PATHS = (
    '%s/locale' % BASE_DIR,
)

DJANGO_WEBVIDEO_SETTINGS = {
    'ffmpeg': {
        'binary': '/usr/bin/ffmpeg'
    },
}
