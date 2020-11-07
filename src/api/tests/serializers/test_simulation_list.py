from django import test
from django.test import RequestFactory
from django.test.utils import override_settings
from django.urls import path, include, reverse
from django.utils import timezone

from api.models.models import LAWMSimulation
from api.serializers.simulation_serializers import SimulationListSerializer
from api.tests.api_test_mixin import MicroSimuTestMixin

# The hyperlinked serializer depends on the urls, so we need to specify the urls
test_patterns = [
    path('test_path/'         , lambda request: None, name='simulations'),
    path('test_path/<int:pk>/', lambda request: None  , name='simulation-detail'),
]

urlpatterns = [
    path('', include((test_patterns, "api"))),
]


@override_settings(ROOT_URLCONF=__name__)
class SimulationListSerializerTest(test.TestCase, MicroSimuTestMixin):
    @classmethod
    def setUpTestData(cls):
        cls.request_context = cls.get_request_context()
        cls.before_creation_time_iso = timezone.localtime().isoformat()
        cls.simus = cls.create_multiple_simulations()
        cls.data  = cls.get_serialized_simulations_data(cls.simus)

    def test_correct_fields(self):

        expected_fields = {"created", "url"}

        for simu_data in self.data:
            actual_fields = simu_data.keys()
            self.assertEqual(expected_fields, actual_fields)

    def test_serializer_returns_correct_urls(self):
        expected_simus_ids = [simu.id for simu in self.simus]
        for expected_id, actual_data in zip(expected_simus_ids, self.data):
            expected_url = f"{self.BASE_SERVER_URL}/test_path/{expected_id}/"
            self.assertEqual(actual_data["url"], expected_url)

    def test_list_serializer_many_simulations_returns_correct_time(self):
        for simulation in self.data:
            actual_creation_time_iso = simulation["created"]
            self.assert_is_later_and_close(actual_creation_time_iso, self.before_creation_time_iso)

    def test_one_simu_still_returns_list(self):
        simu = LAWMSimulation.objects.create()
        simus = [simu]

        serializer = SimulationListSerializer(simus, many=True, context={'request': None})

        data = serializer.data
        self.assert_has_length(data, 1)
        self.assertEqual(data[0]["url"], f"/test_path/{simu.id}/")

    @classmethod
    def get_serialized_simulations_data(cls, simus):
        serializer = SimulationListSerializer(simus, many=True, context=cls.request_context)
        data = serializer.data
        return data

    @staticmethod
    def create_multiple_simulations():
        simus = [LAWMSimulation.objects.create() for _ in range(3)]
        return simus

    @staticmethod
    def get_request_context():
        url = reverse("api:simulations")
        request_factory = RequestFactory()
        context = {'request': request_factory.get(url)}
        return context
