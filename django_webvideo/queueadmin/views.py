# coding=utf-8
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import login as admin_login, logout as admin_logout
from django.shortcuts import render, redirect
from rq import Worker, Queue
from django_webvideo.queue import redis_conn, get_queue_object


@permission_required('is_superuser', login_url="django_webvideo:queueadmin:login")
def index(request):
    workers = Worker.all(redis_conn)
    queues = Queue.all(redis_conn)
    convert_queue = get_queue_object()
    if not convert_queue in queues:
        queues.append(convert_queue)
    return render(
        request,
        'django_webvideo/queueadmin/index.html',
        {
            'workers': workers,
            'queues': queues,
        }
    )


def login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            admin_login(request=request, user=user)
            if request.POST.get('next', ''):
                return redirect(request.POST.get('next'))
            return redirect('django_webvideo:queueadmin:index')
    return render(request, 'django_webvideo/queueadmin/login.html', {'next': request.GET.get('next', '')})


def logout(request):
    admin_logout(request=request)
    return redirect('django_webvideo:queueadmin:index')
