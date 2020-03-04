from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate

class CreatePageTestCase(TestCase):

    # test that index page returns 200
    def test_create_returns_200(self):
        response = self.client.get(reverse("accounts:create"))
        self.assertEqual(response.status_code, 200)

    # test wrong password
    def test_unmatch_password(self):
        response = self.client.post(reverse("accounts:create"), {
            "email": "user@test.com",
            "password1": "test_user_password",
            "password2": "diffent_password"})
        # trop compliqué?
        self.assertIn(
            "password_mismatch", response.context["form"]["password2"].errors.as_json())

    # test that a user is created
    def test_user_created(self):
        email = "user@test.com"
        password = "test_user_password"
        self.assertIsNone(authenticate(username=email,password=password))
        self.client.post(reverse("accounts:create"), {
            "email": email,
            "password1": password,
            "password2": password})
        self.assertIsNotNone(authenticate(username=email,password=password))

    # test that a user is logged
    def test_user_logged(self):
        email = "user@test.com"
        password = "test_user_password"
        response = self.client.post(reverse("accounts:create"), {
            "email": email,
            "password1": password,
            "password2": password})
        self.assertTrue(response.wsgi_request.user.is_authenticated)

