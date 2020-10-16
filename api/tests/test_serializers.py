from datetime import datetime, timedelta

from django import test
from django.utils import timezone

from api.models import Simulation
from api.serializers import SimulationSerializer


class SimulationSerializerTest(test.TestCase):
    def test_serializer_single_simulation_returns_correct_data(self):
        before_creation_time_iso = timezone.localtime().isoformat()
        simulation = Simulation.objects.create()
        serializer = SimulationSerializer(simulation)
        self.assertEqual(serializer.data["id"], 1)
        actual_creation_time_iso = serializer.data["created"]
        self.assertIsClose(actual_creation_time_iso, before_creation_time_iso)

    def test_serializer_many_simulations_returns_correct_data(self):
        before_creation_time_iso = timezone.localtime().isoformat()
        _ = Simulation.objects.create()
        _ = Simulation.objects.create()
        _ = Simulation.objects.create()
        all_simus = Simulation.objects.all()
        serializer = SimulationSerializer(all_simus, many=True)
        for id in range(1, 4):
            simulation = serializer.data[id-1]
            self.assertEqual(simulation["id"], id)
            actual_creation_time_iso = simulation["created"]
            self.assertIsClose(actual_creation_time_iso, before_creation_time_iso)

    def assertIsClose(self, actual_time_iso, expected_time_iso):
        actual_time   = datetime.fromisoformat(actual_time_iso)
        expected_time = datetime.fromisoformat(expected_time_iso)
        actual_timedelta = abs(actual_time - expected_time)
        max_timedelta = timedelta(seconds=10)
        if actual_timedelta > max_timedelta:
            self.fail(f"The expected time {expected_time} is not close to the actual time {actual_time}.")
