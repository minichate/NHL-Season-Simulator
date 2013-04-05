# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Run'
        db.create_table(u'simulator_run', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('run_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'simulator', ['Run'])

        # Adding field 'Simulation.run'
        db.add_column(u'simulator_simulation', 'run',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['simulator.Run'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Run'
        db.delete_table(u'simulator_run')

        # Deleting field 'Simulation.run'
        db.delete_column(u'simulator_simulation', 'run_id')


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
        u'simulator.run': {
            'Meta': {'object_name': 'Run'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'run_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'simulator.simulation': {
            'Meta': {'object_name': 'Simulation'},
            'N': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_playoffs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'my_team': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'out_playoffs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['simulator.Run']", 'null': 'True', 'blank': 'True'}),
            'run_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'simulator': ('picklefield.fields.PickledObjectField', [], {}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['simulator']