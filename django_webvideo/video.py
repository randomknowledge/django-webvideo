# coding: utf-8
import os
import re
import shutil
import tempfile
import subprocess
from django_webvideo import constants
from django_webvideo.settings import get_setting


def convert_video(infile, outfile, codec, quality, original_bitrate, original_width, original_height):
    if not codec in constants.VIDEO_CODECS.keys():
        raise AttributeError("Parameter 'codec' must be in {0}!".format(constants.VIDEO_CODECS.keys))
    commands = get_setting('ffmpeg', 'convert_settings', 'commands', codec)

    if not os.path.exists(os.path.dirname(outfile)):
        os.makedirs(os.path.dirname(outfile))

    tmp_dir = tempfile.mkdtemp()

    settings = get_setting('ffmpeg', 'convert_settings', quality)
    for cmd in commands:
        if quality == 'original':
            video_bitrate = min(original_bitrate, int(settings.get('video_bitrate').replace('k', '')))
            video_max_bitrate = video_bitrate * 2
            video_bufsize = video_max_bitrate
            cmd = cmd.format(
                ffmpeg=get_setting('ffmpeg', 'binary'),
                infile=infile,
                outfile=outfile,
                video_bitrate="{0}k".format(int(video_bitrate)),
                video_max_bitrate="{0}k".format(int(video_max_bitrate)),
                video_bufsize="{0}k".format(int(video_bufsize)),
                video_size=settings.get('video_size').format(
                    original_width=original_width, original_height=original_height
                ),
            )
        else:
            cmd = cmd.format(
                ffmpeg=get_setting('ffmpeg', 'binary'),
                infile=infile,
                outfile=outfile,
                video_bitrate=settings.get('video_bitrate'),
                video_max_bitrate=settings.get('video_max_bitrate'),
                video_bufsize=settings.get('video_bufsize'),
                video_size=settings.get('video_size'),
            )

        try:
            subprocess.check_output(cmd.split(), stderr=subprocess.PIPE, cwd=tmp_dir)
        except AttributeError:
            # fallback for Python 2.6
            subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, cwd=tmp_dir).communicate()
    shutil.rmtree(tmp_dir, ignore_errors=True)
    return os.path.exists(outfile)


def create_screen_image(infile, outfile, second):
    cmd = "{ffmpeg} -itsoffset -{second} -i {infile} -y -vcodec mjpeg -vframes 1 -an -f rawvideo {outfile}".format(
        ffmpeg=get_setting('ffmpeg', "binary"),
        infile=infile,
        second=second,
        outfile=outfile,
    )

    if not os.path.exists(os.path.dirname(outfile)):
        os.makedirs(os.path.dirname(outfile))

    try:
        subprocess.check_output(cmd.split(), stderr=subprocess.PIPE)
    except AttributeError:
        # fallback for Python 2.6
        subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
    except subprocess.CalledProcessError, e:
        print "CalledProcessError:"
        print e
        return False
    return os.path.exists(outfile)


def video_info(infile):
    cmd = "{ffmpeg} -i {infile} -y -f rawvideo -vframes 1 /dev/null".format(
        ffmpeg=get_setting('ffmpeg', "binary"),
        infile=infile,
    )

    try:
        result = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)
    except AttributeError:
        # fallback for Python 2.6
        result = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    except subprocess.CalledProcessError, e:
        result = str(e.output)
    return result


def video_metadata(infile):
    meta = {
        'duration': 0.0,
        'width': 0,
        'height': 0,
        'bitrate': 0.0,
        'framerate': 29.92,
    }

    info = video_info(infile)
    if not info:
        return meta
    info = re.split(r'[\r\n]+', info)

    for line in info:
        line = line.strip()
        duration = re.search(r'Duration: (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>[\d\.]+)', line, re.I)
        size = re.match(r'Stream.*Video:.*,\s*(?P<width>\d+)x(?P<height>\d+)', line, re.I)
        bitrate = re.search(r'bitrate:\s*(?P<bitrate>[\d\.]+)', line, re.I)
        framerate = re.match(r'Stream.*Video:.*,\s*(?P<framerate>[\d\.]+)\s+tbr', line, re.I)

        if duration:
            h = float(duration.group('hours')) * 3600
            m = float(duration.group('minutes')) * 60
            s = float(duration.group('seconds'))
            meta['duration'] = h + m + s
        if bitrate:
            meta['bitrate'] = float(bitrate.group('bitrate'))
        if size:
            meta['width'] = int(size.group('width'))
            meta['height'] = int(size.group('height'))
        if framerate:
            meta['framerate'] = float(framerate.group('framerate'))
    return meta