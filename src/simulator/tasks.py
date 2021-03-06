from celery import task
from simulator.models import Simulation, GameResult
from django.db import transaction

@task()
def add(*args, **kwargs):
    simulation = Simulation.objects.get(pk=args[0])
    
    if simulation.task_id == None:
        return
    
    game_results = simulation.simulator.run()
    for game in game_results:
        game.simulation = simulation
    
    with transaction.commit_on_success():
        GameResult.objects.filter(simulation=simulation).all().delete()
        GameResult.objects.bulk_create(game_results)
    
        simulation.in_playoffs = simulation.simulator.in_playoffs
        simulation.out_playoffs = simulation.simulator.out_playoffs
        simulation.N = simulation.simulator.completed_sims
        simulation.save()
        
        result = add.apply_async(args=[simulation.pk])
        simulation.task_id = result.id
        simulation.save(update_fields=['task_id'])
