# django-webvideo
___
`django-webvideo` is a [Django](https://www.djangoproject.com/) module to convert videos into web video formats.
Converting is handled by [ffmpeg](http://www.ffmpeg.org/) and queued with [rq](http://python-rq.org/).
By now `django-webvideo` can convert to h264, ogg-vorbis and webm.
`django-webvideo` will also create 3 screenshots of each video.

____
## Requirements
* [Django](https://www.djangoproject.com/)
* [easy-thumbnails](https://github.com/SmileyChris/easy-thumbnails)
* [rq](http://python-rq.org/)
* [ffmpeg](http://www.ffmpeg.org/) with libx264, libvorbis, libvpx, libfaac and libvorbis

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

    DEFAULT_SETTINGS = {
        'upload_to': 'videos',  # upload_to parameter for unconverted videos
        'convert_to': 'videos/converted',  # upload_to parameter for converted videos
        'screens_to': 'videos/screens',  # upload_to parameter for video screenshots
        'ffmpeg': {
            'binary': 'ffmpeg',  # path to ffmpeg binary
            'convert_settings': {
                'commands': {
                    'h264': [
                        # ffmpeg call for converting to h264 (first pass)
                        "{ffmpeg} -y -i {infile} -vcodec libx264 -vprofile high -b:v {video_bitrate} "
                        "-maxrate {video_max_bitrate} -bufsize {video_bufsize} "
                        "-vf scale={video_width}:{video_height} -bf 2 -g 100 -an -threads 0 -pass 1 -f mp4 /dev/null",

                        # ffmpeg call for converting to h264 (second pass)
                        "{ffmpeg} -y -i {infile} -vcodec libx264 -vprofile high -b:v {video_bitrate} "
                        "-maxrate {video_max_bitrate} -bufsize {video_bufsize} "
                        "-vf scale={video_width}:{video_height} -bf 2 -g 100 -threads 0 -pass 2 -acodec libfaac -ar 48000 "
                        "-b:a 128k -ac 2 -f mp4 {outfile}"
                    ],
                    'ogv': [
                        # ffmpeg call for converting to ogv (first pass)
                        "{ffmpeg} -y -i {infile} -vcodec libtheora -b:v {video_bitrate} "
                        "-maxrate {video_max_bitrate} -bufsize {video_bufsize} "
                        "-vf scale={video_width}:{video_height} -bf 2 -g 100 -an -threads 0 -pass 1 -f ogg /dev/null",

                        # ffmpeg call for converting to ogv (second pass)
                        "{ffmpeg} -y -i {infile} -vcodec libtheora -b:v {video_bitrate} "
                        "-maxrate {video_max_bitrate} -bufsize {video_bufsize} "
                        "-vf scale={video_width}:{video_height} -bf 2 -g 100 -threads 0 -pass 2 -acodec libvorbis "
                        "-ar 48000 -b:a 128k -ac 2 -f ogg {outfile}",
                    ],
                    'webm': [
                        # ffmpeg call for converting to webm (first pass)
                        "{ffmpeg} -y -i {infile} -codec:v libvpx -quality good -cpu-used 0 -b:v {video_bitrate} "
                        "-qmin 10 -qmax 42 -maxrate {video_max_bitrate} -bufsize {video_bufsize} "
                        "-vf scale={video_width}:{video_height} -bf 2 -g 100 -an -threads 4 -pass 1 -f webm /dev/null",

                        # ffmpeg call for converting to webm (second pass)
                        "{ffmpeg} -y -i {infile} -codec:v libvpx -quality good -cpu-used 0 -b:v {video_bitrate} "
                        "-qmin 10 -qmax 42 -maxrate {video_max_bitrate} -bufsize {video_bufsize} "
                        "-vf scale={video_width}:{video_height} -bf 2 -g 100 -threads 4 -pass 2 -codec:a libvorbis "
                        "-ar 48000 -b:a 128k -ac 2 -f webm {outfile}",
                    ],
                },
                # High Quality settings (will be passed to commands above)
                '1080p': {
                    'video_bitrate': '1792k',
                    'video_max_bitrate': '4000k',
                    'video_bufsize': '4000k',
                    'video_width': '1920',
                    'video_height': '1080',
                },
                # Semi-High Quality settings (will be passed to commands above)
                '720p': {
                    'video_bitrate': '1000k',
                    'video_max_bitrate': '2000k',
                    'video_bufsize': '2000k',
                    'video_width': '1280',
                    'video_height': '720',
                },
                # Medium Quality settings (will be passed to commands above)
                '480p': {
                    'video_bitrate': '500k',
                    'video_max_bitrate': '1000k',
                    'video_bufsize': '1000k',
                    'video_width': '854',
                    'video_height': '480',
                },
                # Low Quality settings (will be passed to commands above)
                '360p': {
                    'video_bitrate': '300k',
                    'video_max_bitrate': '600k',
                    'video_bufsize': '600k',
                    'video_width': '640',
                    'video_height': '360',
                },
            },
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
            'timeout': 600,  # rq queue timeout (in seconds)
        },
        'use_admin': True,  # set to False to disable registering into django admin
    }

Any setting missing in this dictionary will be replaced by the default one.

## Starting the conversion worker
```console
$ rqworker webvideo:convert
```
replace "webvideo" with your 'queue_prefix' setting

## Example Template usage

    {% load webvideo_tags %}
    {% video_tag webvideo_object 720p autoplay=0 controls=1 attributes='id="test"' screen_num=2 %}