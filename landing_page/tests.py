from django.test import Client, TestCase
from django.urls import reverse

from landing_page.api import check_captcha
from unittest.mock import patch


class TestProductsView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_display_get_index(self):
        response = self.client.get(reverse("landing_page:index"))
        self.assertEqual(response.status_code, 200)

    def test_display_post_index(self):
        data = {
            "g-recaptcha-response": "random_captcha",
            "user_email": "random_email",
        }
        response = self.client.post(
            reverse("landing_page:index"),
            data=data,
        )
        self.assertEqual(response.status_code, 200)


class MockResponse:
    def __init__(self):
        self.status_code = 200

    def json(self):
        return {
            "success": True,
            "challenge_ts": 1620671984,
            "hostname": "fake_hostname",
            "error-codes": [],
        }


class TestApi(TestCase):
    @patch("requests.post", return_value=MockResponse())
    def test_post(self, mocked):
        _, response = check_captcha("fake_secret", "fake_captcha")
        self.assertEqual(response["success"], True)
