from django.core.management.base import BaseCommand, CommandError

from substitut_search.utils.fill_db import FillDB
from substitut_search.models import Product

class Command(BaseCommand):
    help = 'Init the database by dowloading the products on OpenFoodFacts.org'

    def add_arguments(self, parser):
        parser.add_argument('n_products', type=int, default=1000)

    def handle(self, *args, **options):
        old_count = Product.objects.count()
        Product.objects.all().delete()
        count = Product.objects.count()
        if count == 0:
            self.stdout.write(self.style.SUCCESS(
                f'Successfully deleted {old_count} products in the database'))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'{count} products still in the database'))
        fill_db = FillDB(nb_products=options['n_products'])
        fill_db.insert_products()
        count = Product.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'Successfully insered {count} products in the database'))