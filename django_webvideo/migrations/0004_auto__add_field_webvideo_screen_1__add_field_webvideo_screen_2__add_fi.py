# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'WebVideo.screen_1'
        db.add_column(u'django_webvideo_webvideo', 'screen_1',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WebVideo.screen_2'
        db.add_column(u'django_webvideo_webvideo', 'screen_2',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WebVideo.screen_3'
        db.add_column(u'django_webvideo_webvideo', 'screen_3',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'WebVideo.screen_1'
        db.delete_column(u'django_webvideo_webvideo', 'screen_1')

        # Deleting field 'WebVideo.screen_2'
        db.delete_column(u'django_webvideo_webvideo', 'screen_2')

        # Deleting field 'WebVideo.screen_3'
        db.delete_column(u'django_webvideo_webvideo', 'screen_3')


    models = {
        u'django_webvideo.webvideo': {
            'Meta': {'object_name': 'WebVideo'},
            'duration': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'h264': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oggvorbis': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'original': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'screen_1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'screen_2': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'screen_3': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['django_webvideo']