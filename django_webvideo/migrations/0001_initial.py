# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WebVideo'
        db.create_table(u'django_webvideo_webvideo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('h264', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('oggtheora', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('duration', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('screen_1', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('screen_2', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('screen_3', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'django_webvideo', ['WebVideo'])


    def backwards(self, orm):
        # Deleting model 'WebVideo'
        db.delete_table(u'django_webvideo_webvideo')


    models = {
        u'django_webvideo.webvideo': {
            'Meta': {'object_name': 'WebVideo'},
            'duration': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'h264': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oggtheora': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'original': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'screen_1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'screen_2': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'screen_3': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['django_webvideo']