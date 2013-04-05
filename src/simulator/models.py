from django.db import models
from picklefield.fields import PickledObjectField

class Simulation(models.Model):
    run_at = models.DateTimeField(auto_now=True)
    N = models.IntegerField()
    my_team = models.CharField(max_length=3)
    in_playoffs = models.IntegerField(null=True, blank=True)
    out_playoffs = models.IntegerField(null=True, blank=True)
    simulator = PickledObjectField()
    task_id = models.CharField(max_length=255, null=True, blank=True)
    
    @property
    def playoff_probability(self):
        return 100 * float(sum(self.simulator.position[:8])) / float(sum(self.simulator.position))
    
    @property
    def non_playoff_probability(self):
        return 100.0 - self.playoff_probability

class GameResult(models.Model):
    simulation = models.ForeignKey(Simulation)
    date = models.DateField()
    home = models.CharField(max_length=3)
    away = models.CharField(max_length=3)
    desired = models.CharField(max_length=3, null=True, blank=True)
    home_win_good = models.IntegerField()
    home_loss_good = models.IntegerField()
    
    @property
    def scenarios(self):
        return self.home_loss_good + self.home_win_good

    @property
    def lift_percentage(self):
        if self.desired == self.home:
            diff = abs(self.scenarios - self.home_win_good)
            return 100 * float(self.home_win_good - diff) / float(self.simulation.N)
        else:
            diff = abs(self.scenarios - self.home_loss_good)
            return 100 * float(self.home_loss_good - diff) / float(self.simulation.N)