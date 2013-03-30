from django.db import models

class Simulation(models.Model):
    run_at = models.DateTimeField(auto_now=True)
    N = models.IntegerField()
    my_team = models.CharField(max_length=3)

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
