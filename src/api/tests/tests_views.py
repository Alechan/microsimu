from django.test import RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.reverse import reverse as drf_reverse
from rest_framework.test import APITestCase

from api.models.models import LAWMSimulation
from api.serializers import SimulationListSerializer, SimulationDetailSerializer, RegionResultSerializer, \
    RunParametersSerializer

from api.std_lib.lawm.regions import Africa
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

    @staticmethod
    def get_view_from_response(response):
        view = response.renderer_context["view"]
        return view

    @classmethod
    def get_metadata_class_from_response(cls, response):
        view = cls.get_view_from_response(response)
        metadata_class = view.metadata_class
        return metadata_class


class ApiRootEndpointTest(ApiViewsTest):
    def setUp(self):
        super().setUpTestData()
        self.url = reverse("api:api_root")
        self.response = self.client.get(self.url)
        self.request  = self.request_factory.get(self.url)
        view = self.get_view_from_response(self.response)
        self.actual_view = view

    def test_api_root_returns_correct_links(self):
        expected_data = {
            "simulations": drf_reverse('api:simulations', request=self.request),
            "simulate"   : drf_reverse('api:simulate'   , request=self.request),
        }
        self.assertEqual(expected_data, self.response.data)

    def test_view_name_is_correct(self):
        expected_view_name = "API"
        self.assertEqual(expected_view_name, self.actual_view.get_view_name())

    def test_description_includes_example_urls(self):
        actual_description = self.actual_view.get_view_description(html=True)
        desc_urls = [
            self.request.build_absolute_uri(reverse("api:simulations")),
            self.request.build_absolute_uri(reverse("api:simulation-detail", args=[1])),
            self.request.build_absolute_uri(reverse("api:regionresult-detail", args=[1, Africa.name])),
        ]
        for url in desc_urls:
            self.assertIn(url, actual_description)


class SimulationsTest(ApiViewsTest):
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


class SimulateTest(ApiViewsTest):
    def setUp(self):
        self.all_simus_before = list(LAWMSimulation.objects.all())
        self.url = reverse("api:simulate")

    def test_simulate_GET_returns_model_parameters(self):
        get_response = self.client.get(self.url)

        expected_fields = {}
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.fail("haceme")

    def test_simulate_POST_triggers_new_simulation(self):
        post_response = self.client.post(self.url)

        new_simu = LAWMSimulation.objects.last()
        expected_all_simus_after = self.all_simus_before + [new_simu]
        actual_all_simus_after   = list(LAWMSimulation.objects.all())

        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(expected_all_simus_after, actual_all_simus_after)
        self.fail("haceme")

    def test_simulate_OPTIONS_returns_correct_metadata(self):
        serializer = RunParametersSerializer()

        options_response     = self.client.options(self.url)
        actual_actions_post  = options_response.data["actions"]["POST"]

        metadater_class_used = self.get_metadata_class_from_response(options_response)
        expected_actions_post = metadater_class_used().get_serializer_info(serializer)

        self.assert_dicts_equal(actual_actions_post, expected_actions_post)


class RegionsEndpointsTest(ApiViewsTest):
    def test_region_result_detail_calls_correct_serializer(self):
        simu_id          = self.simu_1.id
        region_result_id = self.region_result_s1_r1.region.name
        url = reverse("api:regionresult-detail", args=[simu_id, region_result_id])
        response = self.client.get(url)

        context = {'request': self.request_factory.get(url)}

        serializer = RegionResultSerializer(self.region_result_s1_r1, context=context)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
