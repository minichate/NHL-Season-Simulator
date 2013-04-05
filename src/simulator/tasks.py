from celery import task
from simulator.models import Simulation

@task()
def add(*args, **kwargs):
    simulation = Simulation.objects.get(pk=args[0])
    
    if simulation.task_id is None:
        return
    
    simulation.simulator.simulation = simulation
    simulation.simulator.run()
    
    request = add.apply_async(args=[args[0]], countdown=3)
    simulation.task_id = request.id
    simulation.save()
