from django.core.management.base import BaseCommand, CommandError
from simulator.playoffs import PlayoffSimulator
from simulator.models import Simulation
from simulator.tasks import add
from celery.canvas import chain

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        N = 10000
        simulator = PlayoffSimulator()
        
        for team in (simulator.east_points.keys() + simulator.west_points.keys()):
            simulator.init(N, team)
            simulation = Simulation.objects.create(my_team=team, N=0, simulator=simulator).pk
            chain(*[add.si(simulation) for x in range(10)]).apply_async()
            
