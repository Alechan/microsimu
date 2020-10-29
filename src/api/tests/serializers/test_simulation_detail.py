
from django import test
from django.test import override_settings
from django.urls import path, include
from django.utils import timezone

from api.models.models import LAWMSimulation
from api.serializers import SimulationDetailSerializer
from api.tests.api_test_mixin import ApiTestMixin

# The hyperlinked serializer depends on the urls, so we need to specify the urls
test_patterns = [
    path('test_path/<int:pk>/'             , lambda request: None, name='simulation-detail'),
    path('test_path/<int:pk>/<str:region>/', lambda request: None, name='regionresult-detail'),
]

urlpatterns = [
    path('', include((test_patterns, "api"))),
]


@override_settings(ROOT_URLCONF=__name__)
class SimulationDetailSerializerTest(test.TestCase, ApiTestMixin):
    @classmethod
    def setUpTestData(cls):
        db_tree = cls.create_full_simulation_db_tree()
        cls.simu = db_tree.simu
        cls.region_1 = db_tree.region_1
        cls.region_2 = db_tree.region_2
        serializer = SimulationDetailSerializer(cls.simu, context={'request': None})
        cls.data = serializer.data

    def test_serializer_returns_correct_fields(self):
        actual_fields_names = self.data.keys()
        expected_fields_names = {'url', 'regions', 'created'}

        self.assertEqual(expected_fields_names, actual_fields_names)

    def test_serializer_returns_correct_id(self):
        simu_id = self.simu.id
        self.assertEqual(self.data["url"], f"/test_path/{simu_id}/")

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
        self.assertEqual(len(regions), 2)
        self.assertEqual(regions[self.region_1.name], f"/test_path/{simu_id}/{self.region_1.name}/")
        self.assertEqual(regions[self.region_2.name], f"/test_path/{simu_id}/{self.region_2.name}/")
