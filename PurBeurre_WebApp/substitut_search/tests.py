from django.test import TestCase
from unittest.mock import Mock
from unittest import skip
import pdb

from .models import Product
from .utils.fill_db import FillDB



class TestFillDB(TestCase):
    MOCK_PRODUCTS = [
        {"nutrition_grade_fr": "a",
        "categories_tags": ["en:test"],
        "product_name": "test1",
        "url": "https//test.com",
        "image_front_url": "https//test.com"},
        {"nutrition_grade_fr": "b",
        "categories_tags": ["en:test"],
        "product_name": "test2",
        "url": "https//test2.com",
        "image_front_url": "https//test2.com"},
    ]

    def tearDown(self):
        for product in Product.objects.all():
                product.delete()

    def test_insert_products(self):
        self.assertEqual(Product.objects.count(), 0)
        fill_db = FillDB()
        fill_db.dl_products = Mock(return_value=self.MOCK_PRODUCTS)
        result = fill_db.insert_products()
        fill_db.dl_products.assert_called_once()
        self.assertQuerysetEqual(
            list(Product.objects.all()),
            ['<Product: test1>','<Product: test2>'])

    @skip("very long test using API call")
    def test_insert_products_no_mock(self):
        self.assertEqual(Product.objects.count(), 0)
        fill_db = FillDB()
        result = fill_db.insert_products()
        pdb.set_trace()
        self.assertGreater(Product.objects.count(), 200)

