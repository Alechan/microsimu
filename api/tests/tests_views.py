from django.test import RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models.models import LAWMSimulation, LAWMYearResult
from api.serializers import SimulationListSerializer, SimulationDetailSerializer
from api.tests.api_test_mixin import ApiTestMixin


class ApiViewsTest(APITestCase, ApiTestMixin):
    def test_simulations_list_calls_correct_serializer(self):
        db_tree_1 = self.create_full_simulation_db_tree()
        db_tree_2 = self.create_full_simulation_db_tree()
        simus = LAWMSimulation.objects.all()

        url = reverse("api:simulations")
        response = self.client.get(url)

        context = {'request': RequestFactory().get(url)}

        serializer = SimulationListSerializer(simus, many=True, context=context)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_simulations_detail_calls_correct_serializer(self):
        db_tree = self.create_full_simulation_db_tree()
        simu = db_tree.simu

        url = reverse("api:simulation-detail", args=[simu.id])
        response = self.client.get(url)

        context = {'request': RequestFactory().get(url)}

        serializer = SimulationDetailSerializer(simu, context=context)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

