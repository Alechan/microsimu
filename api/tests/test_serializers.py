from django import test
from django.utils import timezone

from api.models.models import LAWMSimulation, LAWMResult
from api.serializers import SimulationListSerializer, ResultInstanceSerializer, \
    SimulationDetailSerializer
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
        simu = self.create_simple_db_simulation(pop_values=pop_values)

        serializer = SimulationDetailSerializer(simu)
        simu_serialized = serializer.data

        self.assertEqual(simu_serialized["id"], 1)
        results = simu_serialized["results"]
        self.assertEqual(len(results), len(pop_values))
        for res, pop_value in zip(results, pop_values):
            self.assertEqual(res["pop"], pop_value)

    def test_serializer_returns_correct_fields(self):
        simu = self.create_simple_db_simulation(pop_values=[1, 2])

        serializer = SimulationDetailSerializer(simu)
        simu_serialized = serializer.data

        actual_fields = simu_serialized.keys()
        expected_fields = {x.name for x in serializer.Meta.model._meta.get_fields()}

        self.assertEqual(expected_fields, actual_fields)


class SimulationListSerializerTest(test.TestCase, ApiTestMixin):
    def test_list_serializer_one_simu_still_returns_list(self):
        self.create_simple_db_simulation(pop_values=[1, 2, 3])
        all_simus = LAWMSimulation.objects.all()

        serializer = SimulationListSerializer(all_simus, many=True)
        data = serializer.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], 1)

    def test_list_serializer_returns_correct_fields(self):
        self.create_simple_db_simulation(pop_values=[1])
        self.create_simple_db_simulation(pop_values=[2, 3, 4])
        all_simus = LAWMSimulation.objects.all()

        serializer = SimulationListSerializer(all_simus, many=True)
        data = serializer.data
        expected_fields = {"created", "id"}

        for simu_data in data:
            actual_fields = simu_data.keys()
            self.assertEqual(expected_fields, actual_fields)

    def test_list_serializer_many_simulations_returns_correct_time(self):
        before_creation_time_iso = timezone.localtime().isoformat()
        _ = LAWMSimulation.objects.create()
        _ = LAWMSimulation.objects.create()
        _ = LAWMSimulation.objects.create()
        all_simus = LAWMSimulation.objects.all()

        serializer = SimulationListSerializer(all_simus, many=True)
        data = serializer.data

        for simu_id in range(1, 4):
            simulation = data[simu_id - 1]
            self.assertEqual(simulation["id"], simu_id)
            actual_creation_time_iso = simulation["created"]
            self.assert_is_later_and_close(actual_creation_time_iso, before_creation_time_iso)


class ResultSerializerTest(test.TestCase, ApiTestMixin):
    def test_serializer_result_correct_attributes(self):
        simu = LAWMSimulation.objects.create()
        res = LAWMResult.objects.create(
            simulation=simu,
            pop=1,
            popr=2,
        )

        serializer = ResultInstanceSerializer(res)

        data = serializer.data
        self.assertEqual(data["pop"] , 1)
        self.assertEqual(data["popr"], 2)

