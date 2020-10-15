from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from rest_framework.test import APIClient


class APIStaticLiveServerTestCase(StaticLiveServerTestCase):
    """
    Class to add DRF's APIClient to Django's "auto-collect static files" live server class
    """
    client_class = APIClient


class FunctionalTest(APIStaticLiveServerTestCase):
    def test_simulations_endpoint(self):
        response = self.client.get("/api/simulations/")
        self.assertEqual(response.status_code, 200)
