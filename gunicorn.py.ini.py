# coding=utf-8
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
RUN_DIR = os.path.abspath(
    os.path.join(BASE_DIR, 'run')
)
LOG_DIR = os.path.abspath(
    os.path.join(BASE_DIR, 'log')
)

if not os.path.exists(RUN_DIR):
    os.makedirs(RUN_DIR)

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

bind = "unix:{0}".format(
    os.path.abspath(
        os.path.join(RUN_DIR, 'gunicorn.sock')
    )
)

pidfile = os.path.abspath(
    os.path.join(RUN_DIR, 'gunicorn.pid')
)

workers = 4
worker_class = 'gevent'
worker_connections = 1000
errorlog = os.path.abspath(
    os.path.join(BASE_DIR, 'log', 'gunicorn.error.log')
)
accesslog = os.path.abspath(
    os.path.join(BASE_DIR, 'log', 'gunicorn.access.log')
)
proc_name = 'webvideo_gunicorn'
pythonpath = ":".join((
    os.path.abspath(
        os.path.join(BASE_DIR, 'virtualenv')
    ),
    os.path.abspath(
        os.path.join(BASE_DIR)
    ),
))

preload_app = True
loglevel = "info"