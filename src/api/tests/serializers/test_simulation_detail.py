
from django import test
from django.test import override_settings, RequestFactory
from django.urls import path, include, reverse
from django.utils import timezone

from api.models.models import LAWMSimulation
from api.serializers.parameters_serializers import RunParametersSerializer
from api.serializers.simulation_serializers import SimulationDetailSerializer
from api.tests.helpers.api_test_mixin import MicroSimuTestMixin

# The hyperlinked serializer depends on the urls, so we need to specify the urls
test_patterns = [
    path('test_path/<int:pk>/'             , lambda request: None, name='simulation-detail'),
    path('test_path/<int:pk>/<str:region>/', lambda request: None, name='regionresult-detail'),
]

urlpatterns = [
    path('', include((test_patterns, "api"))),
]


@override_settings(ROOT_URLCONF=__name__)
class SimulationDetailSerializerTest(test.TestCase, MicroSimuTestMixin):
    @classmethod
    def setUpTestData(cls):
        db_tree = cls.create_full_simulation_db_tree()
        cls.simu = db_tree.simu
        cls.region_1 = db_tree.region_africa
        cls.region_2 = db_tree.region_developed
        cls.run_params = db_tree.run_parameters
        url = reverse("api:simulation-detail", args=[cls.simu.id])
        context = {'request': RequestFactory().get(url)}
        serializer = SimulationDetailSerializer(cls.simu, context=context)
        cls.data = serializer.data

    def test_serializer_returns_correct_fields(self):
        actual_fields_names = self.data.keys()
        expected_fields_names = {'url', 'regions', 'created', "parameters"}

        self.assertEqual(expected_fields_names, actual_fields_names)

    def test_serializer_returns_correct_parameters(self):
        expected_params = RunParametersSerializer(self.run_params).data

        actual_params = self.data["parameters"]

        self.assert_not_empty(actual_params)
        self.assertEqual(actual_params, expected_params)

    def test_serializer_returns_correct_url(self):
        simu_id = self.simu.id
        expected_url = f"{self.BASE_SERVER_URL}/test_path/{simu_id}/"
        self.assertEqual(self.data["url"], expected_url)

    def test_serializer_returns_correct_time(self):
        before_creation_time_iso = timezone.localtime().isoformat()
        new_simu = LAWMSimulation.objects.create()

        new_simu_serializer = SimulationDetailSerializer(new_simu, context={'request': None})
        new_simu_serialized_data = new_simu_serializer.data

        self.assertEqual(new_simu_serialized_data["url"], f"/test_path/{new_simu.id}/")
        actual_creation_time_iso = new_simu_serializer.data["created"]
        self.assert_is_later_and_close(actual_creation_time_iso, before_creation_time_iso)

    def test_serializer_returns_regions(self):
        simu_id = self.simu.id
        regions = self.data["regions"]
        self.assert_has_length(regions, 2)
        self.assertEqual(regions[self.region_1.name], f"{self.BASE_SERVER_URL}/test_path/{simu_id}/{self.region_1.name}/")
        self.assertEqual(regions[self.region_2.name], f"{self.BASE_SERVER_URL}/test_path/{simu_id}/{self.region_2.name}/")
