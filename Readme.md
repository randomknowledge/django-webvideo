# django-webvideo
___
`django-webvideo` is a [Django](https://www.djangoproject.com/) module to convert videos into web video formats.
Converting is handled by [ffmpeg](http://www.ffmpeg.org/) and queued with [rq](http://python-rq.org/).
By now `django-webvideo` can convert to h264 and ogg/theora.
`django-webvideo` will also create 3 screenshots of each video.

____
## Requirements
* [Django](https://www.djangoproject.com/)
* [easy-thumbnails](https://github.com/SmileyChris/easy-thumbnails)
* [rq](http://python-rq.org/)

## Installation

Install [pip](http://pypi.python.org/pypi/pip):

```console
$ sudo easy_install pip
```

Download source and install package using pip:

```console
$ sudo pip install -e git+https://github.com/randomknowledge/django-webvideo.git#egg=django-webvideo
```

Add ``django_webvideo`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        ...
        'django_webvideo',
    )

If you have South installed then run ``manage.py migrate``,
otherwise just run ``manage.py syncdb``.

## Configuration

The following settings can be added to your django settings (these are also the default settings):

    DJANGO_WEBVIDEO_SETTINGS = {
        'upload_to': 'videos', # upload_to parameter for unconverted videos
        'convert_to': 'videos/converted', # upload_to parameter for converted videos
        'screens_to': 'videos/screens', # upload_to parameter for video screenshots
        'ffmpeg': {
            'binary': 'ffmpeg', # path to ffmpeg binary

            # ffmpeg call for converting to h264
            'call_h264': "{ffmpeg} -y -i {infile} -acodec libmp3lame -ar 48000 -ab 128k -ac 2 -vcodec libx264 "
                         "-cmp 256 -subq 7 -trellis 1 -refs 5 -coder 0 -me_range 16 -keyint_min 25 -sc_threshold 40 "
                         "-i_qfactor 0.71 -bt 1200k -maxrate 1200k -bufsize 1200k -rc_eq 'blurCplx^(1-qComp)' "
                         "-qcomp 0.6 -qmin 10 -qmax 51 -qdiff 4 -level 30 -r 30 -g 90 {outfile}",

            # ffmpeg call for converting to ogv
            'call_ogv': '{ffmpeg} -i {infile} -b 1200k -vcodec libtheora -acodec libvorbis -ab 160000 {outfile}',
        },
        'redis': {
            # redis connection settings
            'connection': {
                'db': 0,
                'host': 'localhost',
                'port': 6379,
            },
            'eager': False,  # If True, Tasks are not queued, but executed directly. Use for testing purposes only!
            'queue_prefix': 'webvideo',  # django_webvideo will prefix all (RQ-)Queues with this prefix.
            'timeout': 600, # rq queue timeout (in seconds)
        },
        'use_admin': True, # set to False to disable registering into django admin
    }

Any setting missing in this dictionary will be replaced by the default one.

## Starting the conversion worker
```console
$ rqworker webvideo:convert
```
replace "webvideo" with your 'queue_prefix' setting

## Example Template usage

    {% load webvideo_tags %}
    {% video_tag webvideo_object width=640 height=480 autoplay=0 controls=1 attributes='id="test"' screen_num=2 %}