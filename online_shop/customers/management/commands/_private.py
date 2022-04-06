from argparse import ArgumentParser

from django.core.management import BaseCommand, CommandError

from core.models import User


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('username')

    def handle(self, *args, **options):
        try:
            self.user = User.objects.get(username=options['username'])
        except Exception:
            raise CommandError('This username doesn\'t exist')

