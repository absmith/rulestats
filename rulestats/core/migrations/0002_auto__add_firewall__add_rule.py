# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Firewall'
        db.create_table('core_firewall', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('user', self.gf('django_fields.fields.EncryptedCharField')(max_length=2085, cipher='AES')),
            ('password', self.gf('django_fields.fields.EncryptedCharField')(max_length=2085, cipher='AES')),
            ('enable_password', self.gf('django_fields.fields.EncryptedCharField')(max_length=2085, cipher='AES')),
        ))
        db.send_create_signal('core', ['Firewall'])

        # Adding model 'Rule'
        db.create_table('core_rule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firewall', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rules', to=orm['core.Firewall'])),
            ('access_list', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('protocol', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('details', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('max_hit_count', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('current_hit_count', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('hash1', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('added_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('max_hit_count_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('core', ['Rule'])


    def backwards(self, orm):
        # Deleting model 'Firewall'
        db.delete_table('core_firewall')

        # Deleting model 'Rule'
        db.delete_table('core_rule')


    models = {
        'core.firewall': {
            'Meta': {'object_name': 'Firewall'},
            'enable_password': ('django_fields.fields.EncryptedCharField', [], {'max_length': '2085', 'cipher': "'AES'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'password': ('django_fields.fields.EncryptedCharField', [], {'max_length': '2085', 'cipher': "'AES'"}),
            'user': ('django_fields.fields.EncryptedCharField', [], {'max_length': '2085', 'cipher': "'AES'"})
        },
        'core.rule': {
            'Meta': {'object_name': 'Rule'},
            'access_list': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'added_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_hit_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'firewall': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rules'", 'to': "orm['core.Firewall']"}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'hash1': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'max_hit_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'max_hit_count_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['core']