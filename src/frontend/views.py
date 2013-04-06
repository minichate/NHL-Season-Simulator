from django.http import HttpResponse
from simulator.tasks import add
from simulator.playoffs import PlayoffSimulator
from simulator.models import Simulation, Run
from django.shortcuts import render_to_response
from django.http.response import HttpResponsePermanentRedirect
from celery.task.control import revoke, discard_all
import copy

teams = sorted([u'ANA', u'BOS', u'BUF', u'CAR', u'CBJ', u'CGY', u'CHI', u'COL', u'DAL', u'DET', u'EDM', u'FLA', u'LAK', u'MIN', u'MTL', u'NJD', u'NSH', u'NYI', u'NYR', u'OTT', u'PHI', u'PHX', u'PIT', u'SJS', u'STL', u'TBL', u'TOR', u'VAN', u'WPG', u'WSH'])

def kickoff(request):
    stop_all(request)
    
    N = 5000
    simulator = PlayoffSimulator()
    run = Run.objects.create()
    
    stop_all(request)
    
    for team in (simulator.east_points.keys() + simulator.west_points.keys()):
        simulator_copy = copy.copy(simulator)
        simulator_copy.init(N, team)
        simulation = Simulation.objects.create(my_team=team, N=0, simulator=simulator_copy, run=run)
        result = add.apply_async(args=[simulation.pk])
        simulation.task_id = result.id
        simulation.save(update_fields=['task_id'])
        
    return HttpResponse("kicked off all")

def stop_all(request):
    discard_all()
    
    active_sims = Simulation.objects.filter(task_id__isnull=False).all()
    for simulation in active_sims:
        revoke(simulation.task_id, terminate=True)
        simulation.task_id = None
        simulation.save(update_fields=['task_id'])
        
    discard_all()
    
    return HttpResponse("stopped all")
    
def show_results(request):
    
    if 'team' in request.GET:
        my_team = request.GET['team'].upper()
    else:
        my_team = 'TOR'
        
    query = Run.objects.order_by('-run_at')[0].simulation_set.filter(my_team=my_team)
    
    if query.count() == 0:
        return HttpResponsePermanentRedirect('/')
        
    simulation = query[0]
    game_results = simulation.gameresult_set.order_by('date').all()
    
    return render_to_response('results.html',
                              {'game_results': game_results,
                               'simulation': simulation,
                               'teams': teams,
                               'my_team': my_team})
    
    
