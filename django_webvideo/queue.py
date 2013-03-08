# coding=utf-8
from django_webvideo.settings import get_setting, get_queue_name
from rq import Queue
from redis import Redis


redis_conn = Redis(
    host=get_setting('redis', 'connection', 'host'),
    db=get_setting('redis', 'connection', 'db'),
    port=get_setting('redis', 'connection', 'port'),
)


def enqueue(func, *args, **kwargs):
    if get_setting('redis', 'eager'):
        func(*args, **kwargs)
    else:
        q = Queue(connection=redis_conn, name=get_queue_name(), default_timeout=get_setting('redis', 'timeout'))
        q.enqueue(func, *args, **kwargs)