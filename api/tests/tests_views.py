from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models.models import LAWMSimulation, LAWMResult
from api.serializers import SimulationListSerializer
from api.tests.api_test_mixin import ApiTestMixin


class ApiViewsTest(APITestCase, ApiTestMixin):
    def test_simulations_calls_correct_serializer(self):
        self.create_simple_db_simulation(pop_values=[1])
        self.create_simple_db_simulation(pop_values=[2, 3, 4])
        simus = LAWMSimulation.objects.all()

        url = reverse("api:simulations")
        response = self.client.get(url)

        serializer = SimulationListSerializer(simus, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

