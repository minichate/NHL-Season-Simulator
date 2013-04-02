from django.core.management.base import BaseCommand, CommandError
from simulator.playoffs import PlayoffSimulator
from simulator.models import Simulation
from simulator.tasks import add
from celery.canvas import chain
from frontend.views import kickoff


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        kickoff(None)
