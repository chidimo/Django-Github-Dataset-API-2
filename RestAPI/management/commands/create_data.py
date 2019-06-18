import os
import json
import glob

import django
from django.conf import settings
from django.core.management.base import BaseCommand#, CommandError

from RestAPI.views import create_events_data

DATA_STORE = os.path.join(settings.BASE_DIR, 'TestData')
data_files = glob.glob('{}/*.json'.format(DATA_STORE))

class Command(BaseCommand):
    help = 'Create events data, optional specify number of data to add'

    def add_arguments(self, parser):
        parser.add_argument('-num', type=int)


    def handle(self, *args, **options):

        num = options['num'] if options['num'] else ''
        data = []

        for each in data_files:
            with open(each, 'r+') as f:
                for line in f:
                    js = json.loads(line)
                    if js['request']['method'] == "POST": 
                        data.append(json.loads(line))

        if options['num']:
            data = data[:num]

        for item in data:
            body = item['request']['body']
            message, status = create_events_data(body)
            if status == 201:
                self.stdout.write(self.style.SUCCESS(status))
            else:
                self.stdout.write(self.style.ERROR(status))
        self.stdout.write(self.style.SUCCESS('Finished creating data'))
