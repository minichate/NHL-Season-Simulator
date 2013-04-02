# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Simulation'
        db.create_table(u'simulator_simulation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('run_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('N', self.gf('django.db.models.fields.IntegerField')()),
            ('my_team', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('in_playoffs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('out_playoffs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'simulator', ['Simulation'])

        # Adding model 'GameResult'
        db.create_table(u'simulator_gameresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('simulation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['simulator.Simulation'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('home', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('away', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('desired', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('home_win_good', self.gf('django.db.models.fields.IntegerField')()),
            ('home_loss_good', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'simulator', ['GameResult'])


    def backwards(self, orm):
        # Deleting model 'Simulation'
        db.delete_table(u'simulator_simulation')

        # Deleting model 'GameResult'
        db.delete_table(u'simulator_gameresult')


    models = {
        u'simulator.gameresult': {
            'Meta': {'object_name': 'GameResult'},
            'away': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'desired': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'home': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'home_loss_good': ('django.db.models.fields.IntegerField', [], {}),
            'home_win_good': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'simulation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['simulator.Simulation']"})
        },
        u'simulator.simulation': {
            'Meta': {'object_name': 'Simulation'},
            'N': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_playoffs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'my_team': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'out_playoffs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'run_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['simulator']