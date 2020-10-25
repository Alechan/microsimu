from django import test
from django.utils import timezone

from api.models.models import LAWMSimulation
from api.serializers import SimulationDetailSerializer
from api.tests.api_test_mixin import ApiTestMixin


class SimulationDetailSerializerTest(test.TestCase, ApiTestMixin):
    def test_serializer_returns_correct_time(self):
        before_creation_time_iso = timezone.localtime().isoformat()
        simulation = LAWMSimulation.objects.create()

        serializer = SimulationDetailSerializer(simulation)

        self.assertEqual(serializer.data["id"], 1)
        actual_creation_time_iso = serializer.data["created"]
        self.assert_is_later_and_close(actual_creation_time_iso, before_creation_time_iso)

    def test_serializer_returns_expanded_results(self):
        pop_values = [2, 3, 4]
        simu, _ = self.create_simple_db_simulation(pop_values=pop_values)

        serializer = SimulationDetailSerializer(simu)
        simu_serialized = serializer.data

        self.assertEqual(simu_serialized["id"], 1)
        results = simu_serialized["results"]
        self.assertEqual(len(results), len(pop_values))
        for res, pop_value in zip(results, pop_values):
            self.assertEqual(res["pop"], pop_value)

    def test_serializer_returns_correct_fields(self):
        simu, _ = self.create_simple_db_simulation(pop_values=[1, 2])

        serializer = SimulationDetailSerializer(simu)
        simu_serialized = serializer.data

        actual_fields_names = simu_serialized.keys()
        all_results_fields = serializer.Meta.model._meta.get_fields()
        expected_fields_names = {x.name for x in all_results_fields}

        self.assertEqual(expected_fields_names, actual_fields_names)


