from django.http import HttpResponse
from simulator.tasks import add
from simulator.playoffs import PlayoffSimulator
from simulator.models import Simulation, GameResult
from django.shortcuts import render_to_response
from django.db.models.aggregates import Count

def kickoff(request):
    N = 50000
    simulator = PlayoffSimulator()
    
    for team in simulator.east_points:
        simulation = Simulation.objects.create(my_team=team, N=N)
        add.delay(simulator, simulation, N, team)
        
    for team in simulator.west_points:
        simulation = Simulation.objects.create(my_team=team, N=N)
        add.delay(simulator, simulation, N, team)
    
    return HttpResponse("ok")


def show_results(request):
    
    if 'team' in request.GET:
        my_team = request.GET['team']
    else:
        my_team = 'TOR'
    
    simulation = Simulation.objects.annotate(game_results_count=Count('gameresult')).filter(my_team=my_team, game_results_count__gt=1).order_by('-run_at')[0]
    game_results = GameResult.objects.filter(simulation=simulation).order_by('date')
    
    teams = Simulation.objects.order_by('-run_at').values_list('my_team')[:30]
    teams = sorted([x[0] for x in teams])
    
    return render_to_response('results.html',
                              {'game_results': game_results,
                               'simulation': simulation,
                               'teams': teams,
                               'my_team': my_team})
    
    