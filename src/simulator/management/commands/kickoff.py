from django.core.management.base import BaseCommand, CommandError
from simulator.playoffs import PlayoffSimulator
from simulator.models import Simulation
from simulator.tasks import add

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        N = 50000
        simulator = PlayoffSimulator()
        
        for team in simulator.east_points:
            simulation = Simulation.objects.create(my_team=team, N=N)
            add.delay(simulator, simulation, N, team)
            
        for team in simulator.west_points:
            simulation = Simulation.objects.create(my_team=team, N=N)
            add.delay(simulator, simulation, N, team)