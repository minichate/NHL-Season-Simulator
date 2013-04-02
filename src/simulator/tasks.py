from celery import task
from simulator.models import Simulation

@task()
def add(*args, **kwargs):
    print args
    print kwargs
    simulation = Simulation.objects.get(pk=args[0])
    simulation.N += 1000
    simulation.simulator.simulation = simulation
    simulation.simulator.run()
