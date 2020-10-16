from django.test import TestCase
from django.utils import timezone

from api.models import Simulation


class SimulationTest(TestCase):
    def test_created_time_is_automatically_set_to_now(self):
        # timezone.now() uses UTC and django stores dates in UTC (the serializer re-formats them)
        time_before_creation = timezone.now()
        simulation = Simulation.objects.create()
        time_after_creation = timezone.now()
        self.assertGreater(simulation.created, time_before_creation)
        self.assertGreater(time_after_creation, simulation.created)
