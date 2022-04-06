from django.core.management import CommandError
from ._private import Command as BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        if self.user.is_active:
            raise CommandError('This user is already active!')
        self.user.is_active = True
        self.user.save()
        print(self.style.SUCCESS('USER ACTIVATED'))
