from django.core.management.base import BaseCommand
import seed_data

class Command(BaseCommand):
    help = 'Seeds initial flagship streetwear products and categories'

    def handle(self, *args, **options):
        self.stdout.write('Seeding StyleSphere catalog...')
        try:
            seed_data.seed()
            self.stdout.write(self.style.SUCCESS('Successfully seeded StyleSphere catalog!'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error seeding catalog: {e}'))
