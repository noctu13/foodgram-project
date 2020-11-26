import json
from django.core.management.base import BaseCommand, CommandError
from recipes.models import Ingredient


class Command(BaseCommand):
    help = (
        'Load ingredients from json into database'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'file',
            help='json file to load',
        )

    def handle(self, *args, **options):
        try:
            with open(options['file'], 'r') as f:
                data = json.load(f)
            for item in data:
                Ingredient.objects.create(**item)
        except Exception:
            raise CommandError('Some error occured!')
        self.stdout.write(
            self.style.SUCCESS(
                'Successfully added %s ingredients' % len(data)
            )
        )
