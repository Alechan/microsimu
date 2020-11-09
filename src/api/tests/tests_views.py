from copy import deepcopy
from unittest import skip, mock

from django.test import RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.reverse import reverse as drf_reverse
from rest_framework.test import APITestCase

from api.models.models import LAWMSimulation, LAWMRunParameters
from api.serializers.parameters_serializers import RunParametersSerializer
from api.serializers.results_serializers import RegionResultSerializer
from api.serializers.simulation_serializers import SimulationListSerializer, SimulationDetailSerializer

from api.std_lib.lawm.regions import Africa
from api.std_lib.lawm.simulator.exceptions import ValidInputButSimulationError
from api.tests.helpers.api_test_mixin import MicroSimuTestMixin


class ApiViewsTest(APITestCase, MicroSimuTestMixin):
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


class SimulateNotPOSTTest(ApiViewsTest):
    def setUp(self):
        self.url = reverse("api:simulate")
        self.get_response = self.client.get(self.url)
        self.get_json = self.get_response.json()
        self.expected_get_fields = {"general", "regional"}

    def test_simulate_GET_returns_correct_status(self):
        self.assertEqual(self.get_response.status_code, status.HTTP_200_OK)

    def test_simulate_GET_returns_correct_fields(self):
        actual_fields = self.get_json.keys()
        self.assertEqual(self.expected_get_fields, actual_fields)

    def test_simulate_GET_returns_non_empty_nested_dicts(self):
        for field in self.expected_get_fields:
            sub_dict = self.get_json[field]
            self.assert_not_empty(sub_dict)

    def test_simulate_OPTIONS_returns_correct_metadata(self):
        serializer = RunParametersSerializer()

        options_response     = self.client.options(self.url)
        actual_actions_post  = options_response.data["actions"]["POST"]

        metadater_class_used = self.get_metadata_class_from_response(options_response)
        expected_actions_post = metadater_class_used().get_serializer_info(serializer)

        self.assert_dicts_equal(actual_actions_post, expected_actions_post)


class SimulatePOSTTest(ApiViewsTest):
    @classmethod
    def setUpTestData(cls):
        cls.default_run_parameters = RunParametersSerializer.get_default_serialized_data()
        cls.url = reverse("api:simulate")
        cls.expected_fields = {"general", "regional"}
        cls.all_simus_before          = list(LAWMSimulation.objects.all())
        cls.all_run_parameters_before = list(LAWMRunParameters.objects.all())

    def test_simulate_POST_without_input_returns_error(self):
        post_response = self.client.post(self.url)
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_simulate_POST_with_invalid_input_returns_validators_messages(self):
        expected_response_json = {'general': {
            'simulation_stop': ['Ensure this value is less than or equal to 2050. Send an OPTIONS request'
                                ' for more information.']
        }}
        expected_status_code = status.HTTP_400_BAD_REQUEST

        invalid_values = deepcopy(self.default_run_parameters)
        invalid_values["general"]["simulation_stop"] = 9999

        post_response = self.client.post(self.url, invalid_values, format="json")
        actual_status_code = post_response.status_code
        actual_response_json = post_response.json()

        self.assertEqual(expected_status_code, actual_status_code)
        self.assert_dicts_equal(expected_response_json, actual_response_json)

    def test_simulate_POST_with_valid_input_triggers_new_simulation(self):
        post_response = self.client.post(self.url, self.default_run_parameters, format="json")

        new_simu = LAWMSimulation.objects.last()
        expected_all_simus_after = self.all_simus_before + [new_simu]
        actual_all_simus_after   = list(LAWMSimulation.objects.all())

        # Expect a 302 instead of 303 because browsers use the obsolete way
        # https://stackoverflow.com/questions/5129076/after-a-post-should-i-do-a-302-or-a-303-redirect
        self.assertEqual(post_response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(expected_all_simus_after, actual_all_simus_after)
        expected_redirect_url = reverse('api:simulation-detail', args=(new_simu.id,))
        actual_redirect_url   = post_response.url
        self.assertEqual(expected_redirect_url, actual_redirect_url)

        self.assert_simu_equivalent_to_std_run(new_simu)

    @mock.patch('api.std_lib.lawm.simulator.fortran.lawm_fortran_simulator.LAWMFortranSimulator.simulate')
    def test_simulate_POST_that_makes_simulation_return_an_error_returns_a_descriptive_message(self, mock_simulate):
        mock_simulate.side_effect = ValidInputButSimulationError("The simulation raised an error")
        expected_data = {"error": "The inputs were valid but the simulation still raised an error."}

        post_response = self.client.post(self.url, self.default_run_parameters, format="json")
        actual_data   = post_response.json()
        actual_all_simus_after        = list(LAWMSimulation.objects.all())
        actual_all_run_params_after   = list(LAWMRunParameters.objects.all())

        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, post_response.status_code)
        self.assert_dicts_equal(expected_data, actual_data)
        self.assertEqual(self.all_simus_before, actual_all_simus_after)
        self.assertEqual(self.all_run_parameters_before, actual_all_run_params_after)


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
