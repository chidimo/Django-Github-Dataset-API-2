import json

import django
from django.core.management.base import BaseCommand

from RestAPI.models import Actor, Repo, Event

class Command(BaseCommand):
    help = 'Delete Actor, Repo, and Event data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Deleting data from database'))
        Actor.objects.all().delete()
        Repo.objects.all().delete()
        Event.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted all Actor, Repo, and Event data'))