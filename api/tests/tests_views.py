from django.urls import reverse
from rest_framework.test import APITestCase


class SimulationsTest(APITestCase):
    def test_uses_home_template(self):
        url = reverse("api:simulations")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 201)
        actual_simulations = response.json()["results"]
        self.assertEqual(len(actual_simulations), 3)


