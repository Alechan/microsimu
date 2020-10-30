from django.test import RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models.models import LAWMSimulation
from api.serializers import SimulationListSerializer, SimulationDetailSerializer, RegionResultSerializer
from api.tests.api_test_mixin import ApiTestMixin


class ApiViewsTest(APITestCase, ApiTestMixin):
    @classmethod
    def setUpTestData(cls):
        db_tree_1 = cls.create_full_simulation_db_tree()
        db_tree_2 = cls.create_full_simulation_db_tree()
        cls.simu_1 = db_tree_1.simu
        cls.simu_2 = db_tree_2.simu
        cls.region_result_s1_r1 = db_tree_1.region_result_r1
        cls.request_factory = RequestFactory()

    def test_simulations_list_calls_correct_serializer(self):
        all_simus = LAWMSimulation.objects.all()

        url = reverse("api:simulations")
        response = self.client.get(url)

        context = {'request': self.request_factory.get(url)}

        serializer = SimulationListSerializer(all_simus, many=True, context=context)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_simulations_detail_calls_correct_serializer(self):
        simu_id = self.simu_1.id
        url = reverse("api:simulation-detail", args=[simu_id])
        response = self.client.get(url)

        context = {'request': self.request_factory.get(url)}

        serializer = SimulationDetailSerializer(self.simu_1, context=context)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_region_result_detail_calls_correct_serializer(self):
        simu_id          = self.simu_1.id
        region_result_id = self.region_result_s1_r1.region.name
        url = reverse("api:regionresult-detail", args=[simu_id, region_result_id])
        response = self.client.get(url)

        context = {'request': self.request_factory.get(url)}

        serializer = RegionResultSerializer(self.region_result_s1_r1, context=context)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
