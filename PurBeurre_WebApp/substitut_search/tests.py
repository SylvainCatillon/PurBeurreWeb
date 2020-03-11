from django.test import TestCase
from django.urls import reverse

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
        "image_front_small_url": "https//test.com"},
        {"nutrition_grade_fr": "b",
        "categories_tags": ["en:test"],
        "product_name": "test2",
        "url": "https//test2.com",
        "image_front_small_url": "https//test2.com"},
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
            ['<Product: Test1>','<Product: Test2>'])

    @skip("very long test using API call")
    def test_insert_products_no_mock(self):
        self.assertEqual(Product.objects.count(), 0)
        fill_db = FillDB()
        result = fill_db.insert_products()
        pdb.set_trace()
        self.assertGreater(Product.objects.count(), 200)

class TestSearchProduct(TestCase):
    MOCK_PRODUCTS = [
        {"nutrition_grade_fr": "a",
        "categories_tags": ["en:test"],
        "product_name": "test1",
        "url": "https//test.com",
        "image_front_small_url": "https//test.com"},
        {"nutrition_grade_fr": "b",
        "categories_tags": ["en:test"],
        "product_name": "test2",
        "url": "https//test2.com",
        "image_front_small_url": "https//test2.com"},
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fill_db = FillDB()
        fill_db.dl_products = Mock(return_value=cls.MOCK_PRODUCTS)
        fill_db.insert_products()

    # test find a product by name
    def test_find_a_product(self):
        # count how many product the search should find
        query = "test"
        test_products = 0
        for product in self.MOCK_PRODUCTS:
            if query in product["product_name"]:
                test_products += 1
        # test if the search find the right amout of products
        response = self.client.get(
            f"{reverse('substitut:search')}?query={query}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["products"]), test_products)
