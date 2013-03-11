# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VideoScreen'
        db.create_table(u'django_webvideo_videoscreen', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(related_name='screen', to=orm['django_webvideo.WebVideo'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('num', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
        ))
        db.send_create_signal(u'django_webvideo', ['VideoScreen'])

        # Adding unique constraint on 'VideoScreen', fields ['video', 'num']
        db.create_unique(u'django_webvideo_videoscreen', ['video_id', 'num'])

        # Adding model 'ConvertedVideo'
        db.create_table(u'django_webvideo_convertedvideo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('original', self.gf('django.db.models.fields.related.ForeignKey')(related_name='converted', to=orm['django_webvideo.WebVideo'])),
            ('codec', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('quality', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('filesize', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('duration', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('width', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('height', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('bitrate', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('framerate', self.gf('django.db.models.fields.FloatField')(default=29.92)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'django_webvideo', ['ConvertedVideo'])

        # Adding unique constraint on 'ConvertedVideo', fields ['original', 'codec', 'quality']
        db.create_unique(u'django_webvideo_convertedvideo', ['original_id', 'codec', 'quality'])

        # Adding model 'WebVideo'
        db.create_table(u'django_webvideo_webvideo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('filesize', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('duration', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('width', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('height', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('bitrate', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('framerate', self.gf('django.db.models.fields.FloatField')(default=29.92)),
        ))
        db.send_create_signal(u'django_webvideo', ['WebVideo'])


    def backwards(self, orm):
        # Removing unique constraint on 'ConvertedVideo', fields ['original', 'codec', 'quality']
        db.delete_unique(u'django_webvideo_convertedvideo', ['original_id', 'codec', 'quality'])

        # Removing unique constraint on 'VideoScreen', fields ['video', 'num']
        db.delete_unique(u'django_webvideo_videoscreen', ['video_id', 'num'])

        # Deleting model 'VideoScreen'
        db.delete_table(u'django_webvideo_videoscreen')

        # Deleting model 'ConvertedVideo'
        db.delete_table(u'django_webvideo_convertedvideo')

        # Deleting model 'WebVideo'
        db.delete_table(u'django_webvideo_webvideo')


    models = {
        u'django_webvideo.convertedvideo': {
            'Meta': {'unique_together': "(('original', 'codec', 'quality'),)", 'object_name': 'ConvertedVideo'},
            'bitrate': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'codec': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'duration': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'filesize': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'framerate': ('django.db.models.fields.FloatField', [], {'default': '29.92'}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'converted'", 'to': u"orm['django_webvideo.WebVideo']"}),
            'quality': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'video': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'django_webvideo.videoscreen': {
            'Meta': {'unique_together': "(('video', 'num'),)", 'object_name': 'VideoScreen'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'num': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'screen'", 'to': u"orm['django_webvideo.WebVideo']"})
        },
        u'django_webvideo.webvideo': {
            'Meta': {'object_name': 'WebVideo'},
            'bitrate': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'duration': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'filesize': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'framerate': ('django.db.models.fields.FloatField', [], {'default': '29.92'}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['django_webvideo']