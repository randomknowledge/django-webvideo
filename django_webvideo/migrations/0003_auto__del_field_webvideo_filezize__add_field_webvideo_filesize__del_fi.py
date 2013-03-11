# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'WebVideo.filezize'
        db.delete_column(u'django_webvideo_webvideo', 'filezize')

        # Adding field 'WebVideo.filesize'
        db.add_column(u'django_webvideo_webvideo', 'filesize',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'ConvertedVideo.filezize'
        db.delete_column(u'django_webvideo_convertedvideo', 'filezize')

        # Adding field 'ConvertedVideo.filesize'
        db.add_column(u'django_webvideo_convertedvideo', 'filesize',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'WebVideo.filezize'
        db.add_column(u'django_webvideo_webvideo', 'filezize',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'WebVideo.filesize'
        db.delete_column(u'django_webvideo_webvideo', 'filesize')

        # Adding field 'ConvertedVideo.filezize'
        db.add_column(u'django_webvideo_convertedvideo', 'filezize',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'ConvertedVideo.filesize'
        db.delete_column(u'django_webvideo_convertedvideo', 'filesize')


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