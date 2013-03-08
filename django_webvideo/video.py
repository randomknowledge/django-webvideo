# coding: utf-8
import os
import shutil
import tempfile
import subprocess
from django_webvideo import constants
from django_webvideo.settings import get_setting


def convert_video(infile, outfile, codec, quality):
    if not codec in constants.VIDEO_CODECS.keys():
        raise AttributeError("Parameter 'codec' must be in {0}!".format(constants.VIDEO_CODECS.keys))
    commands = get_setting('ffmpeg', 'convert_settings', 'commands', codec)

    if not os.path.exists(os.path.dirname(outfile)):
        os.makedirs(os.path.dirname(outfile))

    tmp_dir = tempfile.mkdtemp()

    settings = get_setting('ffmpeg', 'convert_settings', quality)
    for cmd in commands:
        cmd = cmd.format(
            ffmpeg=get_setting('ffmpeg', 'binary'),
            infile=infile,
            outfile=outfile,
            video_bitrate=settings.get('video_bitrate'),
            video_max_bitrate=settings.get('video_max_bitrate'),
            video_bufsize=settings.get('video_bufsize'),
            video_width=settings.get('video_width'),
            video_height=settings.get('video_height'),
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
