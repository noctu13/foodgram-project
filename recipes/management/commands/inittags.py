from django.core.management.base import BaseCommand, CommandError
from recipes.models import Tag


class Command(BaseCommand):
    help = (
        'Create three Tags: breakfast, lunch, dinner'
    )

    def handle(self, *args, **options):
        try:
            Tag.objects.create(name='Завтрак', color='orange')
            Tag.objects.create(name='Обед', color='green')
            Tag.objects.create(name='Ужин', color='purple')
        except Exception:
            raise CommandError('Some error occured!')
        self.stdout.write(
            self.style.SUCCESS('Successfully added tags')
        )
