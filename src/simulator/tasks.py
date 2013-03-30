from celery import task

@task()
def add(simulator, simulation, N, MY_TEAM):
    simulator.run(simulation, N, MY_TEAM)
