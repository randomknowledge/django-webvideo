# coding=utf-8
from setuptools import setup
import django_webvideo
import finddata


setup(
    name="django-webvideo",
    author="Florian Finke",
    author_email="flo@randomknowledge.org",
    version=django_webvideo.__version__,
    packages=['django_webvideo'],
    package_data=finddata.find_package_data(),
    url='https://github.com/randomknowledge/django-webvideo',
    include_package_data=True,
    license='MIT',
    description='A queuing web video converter',
    long_description=open('Readme.md').read(),
    zip_safe=False,
    install_requires=[
        'Django==1.5',
        'South==0.7.6',
        'PIL==1.1.7',
        'easy-thumbnails==1.2',
        'rq==0.3.7',
        'django-tastypie==0.9.12',
        'django-suit==0.1.6',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
)
