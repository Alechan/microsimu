from django import test
from django.utils import timezone

from api.serializers import SimulationDetailSerializer
from api.std_lib.lawm.variables import Population
from api.tests.api_test_mixin import ApiTestMixin


class SimulationDetailSerializerTest(test.TestCase, ApiTestMixin):
    @classmethod
    def setUpTestData(cls):
        cls.pop_values = [2, 3, 4]
        cls.simu, cls.results = cls.create_simple_db_simulation(pop_values=cls.pop_values)
        cls.serializer = SimulationDetailSerializer(cls.simu)
        cls.simu_serialized = cls.serializer.data

    def test_serializer_returns_correct_fields(self):
        actual_fields_names = self.simu_serialized.keys()
        expected_fields_names = {'id', 'results', 'variables', 'created'}

        self.assertEqual(expected_fields_names, actual_fields_names)

    def test_serializer_returns_correct_id(self):
        self.assertEqual(self.simu_serialized["id"], 1)

    def test_serializer_returns_correct_time(self):
        before_creation_time_iso = timezone.localtime().isoformat()
        simulation, _ = self.create_simple_db_simulation(pop_values=[1])

        serializer = SimulationDetailSerializer(simulation)

        self.assertEqual(serializer.data["id"], 2)
        actual_creation_time_iso = serializer.data["created"]
        self.assert_is_later_and_close(actual_creation_time_iso, before_creation_time_iso)

    def test_serializer_returns_expanded_results(self):
        results = self.simu_serialized["results"]
        self.assertEqual(len(results), len(self.pop_values))
        for res, pop_value in zip(results, self.pop_values):
            self.assertEqual(res["pop"], pop_value)

    def test_serializer_returns_variables(self):
        variables = self.simu_serialized["variables"]
        self.assertEqual(len(variables), 44)
        self.assertEqual(
            variables["pop"],
            Population.info_as_dict()
        )


