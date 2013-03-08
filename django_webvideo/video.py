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

