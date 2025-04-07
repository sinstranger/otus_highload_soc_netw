from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates tables'

    def handle(self, *args, **options):
        print('!!!!!!!!!!!!!!!!!!!!!!')
