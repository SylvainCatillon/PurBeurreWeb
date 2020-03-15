from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from unittest.mock import Mock
from unittest import skip

import pdb

from .models import Product, Favory
from .utils.fill_db import FillDB

nutrients = ['fat','saturated-fat','sugars','salt']
MOCK_PRODUCTS = [
        {"nutrition_grade_fr": "a",
        "categories_tags": ["en:test"],
        "product_name": "test1",
        "url": "https//test.com",
        "image_front_small_url": "https//test.com",
        "nutrient_levels": {e: "low" for e in nutrients},
        'nutriments': {e+'_100g': '2' for e in nutrients}},
        {"nutrition_grade_fr": "b",
        "categories_tags": ["en:test"],
        "product_name": "test2",
        "url": "https//test2.com",
        "image_front_small_url": "https//test2.com"},
    ]

class TestFillDB(TestCase):

    def tearDown(self):
        Product.objects.all().delete()

    def test_insert_products(self):
        self.assertEqual(Product.objects.count(), 0)
        fill_db = FillDB()
        fill_db.dl_products = Mock(return_value=MOCK_PRODUCTS)
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
        self.assertGreater(Product.objects.count(), 200)

class TestSearchProduct(TestCase):
    

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fill_db = FillDB()
        fill_db.dl_products = Mock(return_value=MOCK_PRODUCTS)
        fill_db.insert_products()
    
    @classmethod
    def tearDownClass(cls):
        for product in Product.objects.all():
                product.delete()
        super().tearDownClass()

    # test find a product by name
    def test_find_a_product(self):
        # count how many product the search should find
        query = "test"
        test_products = 0
        for product in MOCK_PRODUCTS:
            if query in product["product_name"]:
                test_products += 1
        # test if the search find the right amout of products
        response = self.client.get(
            f"{reverse('substitut:search')}?query={query}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["products"]), test_products)

    # test if the founded substitut has a better nutriscore and is in the same category
    def test_find_a_substitut(self):
        product = Product.objects.order_by('-nutriscore')[0]
        response = self.client.get(
            f"{reverse('substitut:find')}?product_id={product.id}")
        self.assertLess(
            response.context['products'][0].nutriscore, product.nutriscore)

class TestProductPage(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fill_db = FillDB()
        fill_db.dl_products = Mock(return_value=MOCK_PRODUCTS[:1])
        fill_db.insert_products()

    @classmethod
    def tearDownClass(cls):
        for product in Product.objects.all():
                product.delete()
        super().tearDownClass()

    # test product page contains the required informations    
    def test_product_page(self):
        product = Product.objects.get(
            name=MOCK_PRODUCTS[0]["product_name"].title())
        product_id = product.id
        response = self.client.get(
            f"{reverse('substitut:detail')}?product_id={product_id}")
        self.assertContains(response, product.name)
        self.assertContains(response, product.nutriscore)
        self.assertContains(response, product.link)
        for level in product.nutrient_levels:
            self.assertContains(response, level)


class TestFavories(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_info = {
                "username": "test_user",
                "email": "user@test.com",
                "password": "test_user_password",
                "first_name": "Paul"}
        cls.user = User.objects.create_user(**cls.user_info)
        fill_db = FillDB()
        fill_db.dl_products = Mock(return_value=MOCK_PRODUCTS)
        fill_db.insert_products() 
        cls.product = Product.objects.get(
            name=MOCK_PRODUCTS[0]["product_name"].title())

    def setUp(self):
        self.client.login(
            username=self.user.username, password=self.user_info["password"])

    def tearDown(self):
        Favory.objects.all().delete()

    # test a loged user see the button "save" and an unloged don't
    def test_save_button(self):
        product = Product.objects.order_by('-nutriscore')[0]
        response = self.client.get(
            f"{reverse('substitut:find')}?product_id={product.id}")
        self.assertContains(response, 'class="save_form')
        self.client.logout()
        response = self.client.get(
            f"{reverse('substitut:find')}?product_id={product.id}")
        # save_form contenu dans le script js
        self.assertNotContains(response, 'class="save_form')

    # test a favory is saved
    def test_save_favory(self):
        product_id = self.product.id
        response = self.client.post(
            reverse("substitut:favories"), {"product_id": product_id})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            list(self.user.profile.favories.all()), ['<Product: Test1>'])

    # test a user can see his favories
    def test_see_favories(self):
        self.user.profile.favories.add(self.product)
        response = self.client.get(reverse("substitut:favories"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
