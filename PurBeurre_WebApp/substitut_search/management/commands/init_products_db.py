from django.core.management.base import BaseCommand, CommandError
from substitut_search.utils.fill_db import FillDB

class Command(BaseCommand):
    help = 'Init the database by dowloading the products on OpenFoodFacts.org'

    def add_arguments(self, parser):
        parser.add_argument('n_products', type=int, default=1000)

    def handle(self, *args, **options):
        fill_db = FillDB(nb_products=options['n_products'])
        count = fill_db.insert_products()
        self.stdout.write(self.style.SUCCESS(
            f'Successfully insered {count} products in the database'))