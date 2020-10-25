from django import test
from django.test.utils import override_settings
from django.urls import path, include
from django.utils import timezone

from api.models.models import LAWMSimulation
from api.serializers import SimulationListSerializer
from api.tests.api_test_mixin import ApiTestMixin

# The hyperlinked serializer depends on the urls, so we need to specify the urls
test_patterns = [
    path('test_path/<int:pk>/', lambda request: None, name='simulation-detail'),
]

urlpatterns = [
    path('', include((test_patterns, "api"))),
]


@override_settings(ROOT_URLCONF=__name__)
class SimulationListSerializerTest(test.TestCase, ApiTestMixin):
    def test_list_serializer_one_simu_still_returns_list(self):
        self.create_simple_db_simulation(pop_values=[1, 2, 3])
        all_simus = LAWMSimulation.objects.all()

        serializer = SimulationListSerializer(all_simus, many=True, context={'request': None})

        data = serializer.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], "/test_path/1/")

    def test_list_serializer_returns_correct_fields(self):
        self.create_simple_db_simulation(pop_values=[1])
        self.create_simple_db_simulation(pop_values=[2, 3, 4])
        all_simus = LAWMSimulation.objects.all()

        serializer = SimulationListSerializer(all_simus, many=True, context={'request': None})
        data = serializer.data
        expected_fields = {"created", "url"}

        for simu_data in data:
            actual_fields = simu_data.keys()
            self.assertEqual(expected_fields, actual_fields)

    def test_list_serializer_many_simulations_returns_correct_time(self):
        before_creation_time_iso = timezone.localtime().isoformat()
        _ = LAWMSimulation.objects.create()
        _ = LAWMSimulation.objects.create()
        _ = LAWMSimulation.objects.create()
        all_simus = LAWMSimulation.objects.all()

        serializer = SimulationListSerializer(all_simus, many=True, context={'request': None})
        data = serializer.data

        for simu_id in range(1, 4):
            simulation = data[simu_id - 1]
            self.assertEqual(simulation["url"], f"/test_path/{simu_id}/")
            actual_creation_time_iso = simulation["created"]
            self.assert_is_later_and_close(actual_creation_time_iso, before_creation_time_iso)
