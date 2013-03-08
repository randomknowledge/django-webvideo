# coding: utf-8
import os
from django_webvideo.settings import get_setting
import subprocess


def convert_video(infile, outfile, codec):
    if not codec in ('h264', 'ogv'):
        raise AttributeError("Parameter 'codec' must be either 'h264' or 'ogv'!")
    cmd = get_setting('ffmpeg', "call_{0}".format(codec)).format(
        ffmpeg=get_setting('ffmpeg', 'binary'),
        infile=infile,
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
