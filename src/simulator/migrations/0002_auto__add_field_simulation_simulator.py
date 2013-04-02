# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Simulation.simulator'
        db.add_column(u'simulator_simulation', 'simulator',
                      self.gf('picklefield.fields.PickledObjectField')(default=None),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Simulation.simulator'
        db.delete_column(u'simulator_simulation', 'simulator')


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
            'run_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'simulator': ('picklefield.fields.PickledObjectField', [], {})
        }
    }

    complete_apps = ['simulator']