from django.core.management.base import BaseCommand, CommandError, no_translations
from ._factory_items import start


class Command(BaseCommand):
    help = 'Generation records for local testing'

    def add_arguments(self, parser):
        parser.add_argument('ads', nargs='+', type=int)

    @no_translations
    def handle(self, *args, **options):
        for count in options['ads']:
            start(count)
            self.stdout.write(self.style.SUCCESS('Successfully generate "%s"' % count))
