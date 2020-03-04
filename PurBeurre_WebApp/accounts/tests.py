from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class CreatePageTestCase(TestCase):
    def setUp(self):
        self.user = {
                "username": "test_user",
                "email": "user@test.com",
                "password1": "test_user_password",
                "password2": "test_user_password",
                "first_name": "Paul"}

    # test that index page returns 200
    def test_create_returns_200(self):
        response = self.client.get(reverse("accounts:create"))
        self.assertEqual(response.status_code, 200)

    # test wrong password
    def test_unmatch_password(self):
        self.user["password2"] = "unmatch_password"
        response = self.client.post(reverse("accounts:create"), self.user)
        # trop compliqué?
        self.assertIn(
            "password_mismatch", response.context["form"]["password2"].errors.as_json())

    # test that a user is created
    def test_user_created(self):
        self.assertIsNone(authenticate(
            username=self.user["username"], password=self.user["password1"]))
        self.client.post(reverse("accounts:create"), self.user)
        self.assertIsNotNone(authenticate(
            username=self.user["username"], password=self.user["password1"]))

    # test that a user is logged
    def test_user_logged(self):
        response = self.client.post(reverse("accounts:create"), self.user)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

class MyAccountTestCase(TestCase):
    def setUp(self):
        self.user_info = {
                "username": "test_user",
                "email": "user@test.com",
                "password": "test_user_password",
                "first_name": "Paul"}
        self.user = User.objects.create_user(**self.user_info)

    def test_not_logged_user(self):
        response = self.client.get(reverse("accounts:my_account"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 302)

    def test_logged_user(self):
        pass