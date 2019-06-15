from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Create superuser'))
        username = "restapi"
        try:
            su = User(username=username)
            su.is_staff = True
            su.is_superuser = True
            su.is_admin = True
            su.is_active = True
            su.save()
            su.set_password("password")
            su.save()
            self.stdout.write(self.style.SUCCESS('Superuser {} created successfully'.format(username)))
        except IntegrityError:
            su = User.objects.get(username=username)
            self.stdout.write(self.style.ERROR('Superuser {} already exists'.format(username)))
            pass