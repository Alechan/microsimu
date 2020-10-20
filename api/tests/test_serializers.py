from django import test
from django.utils import timezone

from api.models.models import LAWMSimulation, LAWMResult
from api.serializers import SimulationSerializer, ResultSerializer
from api.tests.api_test_mixin import ApiTestMixin


class SimulationSerializerTest(test.TestCase, ApiTestMixin):
    def test_serializer_single_simulation_returns_correct_time(self):
        before_creation_time_iso = timezone.localtime().isoformat()
        simulation = LAWMSimulation.objects.create()

        serializer = SimulationSerializer(simulation)

        self.assertEqual(serializer.data["id"], 1)
        actual_creation_time_iso = serializer.data["created"]
        self.assert_is_later_and_close(actual_creation_time_iso, before_creation_time_iso)

    def test_serializer_many_simulations_returns_correct_time(self):
        before_creation_time_iso = timezone.localtime().isoformat()
        _ = LAWMSimulation.objects.create()
        _ = LAWMSimulation.objects.create()
        _ = LAWMSimulation.objects.create()
        all_simus = LAWMSimulation.objects.all()

        serializer = SimulationSerializer(all_simus, many=True)

        for simu_id in range(1, 4):
            simulation = serializer.data[simu_id - 1]
            self.assertEqual(simulation["id"], simu_id)
            actual_creation_time_iso = simulation["created"]
            self.assert_is_later_and_close(actual_creation_time_iso, before_creation_time_iso)

    def test_serializer_many_simulations_returns_correct_results_ids(self):
        self.create_simple_db_simulations(pop_values=[1])
        self.create_simple_db_simulations(pop_values=[2, 3, 4])
        all_simus = LAWMSimulation.objects.all()

        serializer = SimulationSerializer(all_simus, many=True)
        data = serializer.data

        self.assert_simulation_serialization_is_as_expected(data, simu_id=1, pop_values=[1])
        self.assert_simulation_serialization_is_as_expected(data, simu_id=2, pop_values=[2, 3, 4])

    def assert_simulation_serialization_is_as_expected(self, data, simu_id, pop_values):
        simu = data[simu_id - 1]
        self.assertEqual(simu["id"], simu_id)
        simu_results_ids = simu["results"]
        self.assert_results_id_are_as_expected(simu_results_ids, pop_values)

    def assert_results_id_are_as_expected(self, simu_results_ids, pop_values):
        self.assertEqual(len(simu_results_ids), len(pop_values))
        simu_results = self.get_lawm_results_from_ids(simu_results_ids)
        for simu_result, pop_value in zip(simu_results, pop_values):
            self.assertEqual(simu_result.pop.value, pop_value)


class ResultSerializerTest(test.TestCase, ApiTestMixin):
    def test_serializer_result_correct_attributes(self):
        simu = LAWMSimulation.objects.create()
        res = LAWMResult.objects.create(
            simulation=simu,
            pop=1,
            popr=2,
        )

        serializer = ResultSerializer(res)

        data = serializer.data
        self.assertEqual(data["pop"] , 1)
        self.assertEqual(data["popr"], 2)



