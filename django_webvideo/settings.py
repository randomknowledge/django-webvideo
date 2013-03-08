# coding: utf-8
from django.conf import settings


DEFAULT_SETTINGS = {
    'upload_to': 'videos',  # upload_to parameter for unconverted videos
    'convert_to': 'videos/converted',  # upload_to parameter for converted videos
    'screens_to': 'videos/screens',  # upload_to parameter for video screenshots
    'ffmpeg': {
        'binary': 'ffmpeg',  # path to ffmpeg binary
        'call_h264': "{ffmpeg} -y -i {infile} -acodec libmp3lame -ar 48000 -ab 128k -ac 2 -vcodec libx264 "
                     "-cmp 256 -subq 7 -trellis 1 -refs 5 -coder 0 -me_range 16 -keyint_min 25 -sc_threshold 40 "
                     "-i_qfactor 0.71 -bt 1200k -maxrate 1200k -bufsize 1200k -rc_eq 'blurCplx^(1-qComp)' "
                     "-qcomp 0.6 -qmin 10 -qmax 51 -qdiff 4 -level 30 -r 30 -g 90 {outfile}",
        'call_h264_2': "{ffmpeg} -y -i {infile} -vcodec libx264 -vprofile medium"
                     "-qcomp 0.6 -qmin 10 -qmax 51 -qdiff 4 -level 30 -r 30 -g 90 {outfile}",
        'call_ogv': '{ffmpeg} -i {infile} -b 1200k -vcodec libtheora -acodec libvorbis -ab 160000 {outfile}',

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


def _get_setting(setting, key, *subkeys):
    if len(subkeys) > 0:
        while setting is not None and isinstance(setting, dict) and len(subkeys) > 0:
            setting = setting.get(key)
            key = subkeys[0]
            subkeys = subkeys[1:]
        try:
            return setting.get(key)
        except AttributeError:
            return None
    else:
        return setting.get(key)


def get_setting(key, *subkeys):
    value = _get_setting(getattr(settings, 'DJANGO_WEBVIDEO_SETTINGS'), key, *subkeys)
    if value is None:
        return _get_setting(DEFAULT_SETTINGS, key, *subkeys)
    else:
        return value


def get_queue_name():
    return "{0}:convert".format(get_setting('redis', 'queue_prefix'))