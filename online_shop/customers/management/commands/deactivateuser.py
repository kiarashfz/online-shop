from django.core.management import CommandError
from ._private import Command as BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not self.user.is_active:
            raise CommandError('This user is already deactivate!')
        self.user.is_active = False
        self.user.save()
        print(self.style.ERROR('USER DEACTIVATED'))
