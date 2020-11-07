from django import test
from django.test import override_settings, RequestFactory
from django.urls import path, include, reverse

from api.serializers.results_serializers import RegionResultSerializer
from api.std_lib.lawm.variables import Population
from api.tests.api_test_mixin import MicroSimuTestMixin

test_patterns = [
    path('test_path/<int:pk>/'             , lambda request: None, name='simulation-detail'),
    path('test_path/<int:pk>/<str:region>/', lambda request: None, name='regionresult-detail'),
]

urlpatterns = [
    path('', include((test_patterns, "api"))),
]


@override_settings(ROOT_URLCONF=__name__)
class RegionResultSerializerTest(test.TestCase, MicroSimuTestMixin):
    @classmethod
    def setUpTestData(cls):
        db_tree = cls.create_full_simulation_db_tree()
        cls.simu = db_tree.simu
        cls.region_result = db_tree.region_result_r1
        cls.region_name = cls.region_result.region_name
        url = reverse("api:regionresult-detail", args=[cls.simu.id, cls.region_name])
        context = {'request': RequestFactory().get(url)}
        serializer = RegionResultSerializer(cls.region_result, context=context)
        cls.data = serializer.data

    def test_returns_correct_fields(self):
        expected_fields = {"simulation", "region", "results", "variables"}

        actual_fields = self.data.keys()
        self.assertEqual(expected_fields, actual_fields)

    def test_returns_correct_simulation_url(self):
        simu_id = self.simu.id
        expected_simulation_url = f"{self.BASE_SERVER_URL}/test_path/{simu_id}/"
        self.assertEqual(self.data["simulation"], expected_simulation_url)

    def test_includes_region_name(self):
        self.assertEqual(self.data["region"], self.region_result.region_name)

    def test_returns_expanded_results(self):
        y_1960_values = self.get_year_result_creation_kwargs(self.region_result, year=1960)
        del y_1960_values["region_result"]

        y_1961_values = self.get_year_result_creation_kwargs(self.region_result, year=1961)
        del y_1961_values["region_result"]

        expected_results = [y_1960_values, y_1961_values]
        actual_results = self.data["results"]

        self.assertEqual(expected_results, actual_results)

    def test_serializer_returns_variables(self):
        variables = self.data["variables"]
        self.assert_has_length(variables, 44)
        self.assertEqual(
            variables["pop"],
            Population.info_as_dict()
        )
