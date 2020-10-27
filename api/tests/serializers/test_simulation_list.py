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
    @classmethod
    def setUpTestData(cls):
        data = cls.get_serializer_data_for_multiple_simulations()
        cls.data = data

    def test_correct_fields(self):
        expected_fields = {"created", "url"}

        for simu_data in self.data:
            actual_fields = simu_data.keys()
            self.assertEqual(expected_fields, actual_fields)

    def test_one_simu_still_returns_list(self):
        simu = LAWMSimulation.objects.create()
        simus = [simu]

        serializer = SimulationListSerializer(simus, many=True, context={'request': None})

        data = serializer.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"/test_path/{simu.id}/")

    def test_list_serializer_many_simulations_returns_correct_time(self):
        before_creation_time_iso = timezone.localtime().isoformat()
        data = self.get_serializer_data_for_multiple_simulations()

        for simu_id in range(1, 4):
            simulation = data[simu_id - 1]
            actual_creation_time_iso = simulation["created"]
            self.assert_is_later_and_close(actual_creation_time_iso, before_creation_time_iso)

    @staticmethod
    def get_serializer_data_for_multiple_simulations():
        simus = [LAWMSimulation.objects.create() for _ in range(3)]
        serializer = SimulationListSerializer(simus, many=True, context={'request': None})
        data = serializer.data
        return data

