from django.test import TestCase
from django.utils import timezone

from api.models.models import LAWMSimulation, LAWMResult
from api.std_lib.lawm.variables import Population, PopulationGrowth


class LAWMSimulationTest(TestCase):
    def test_created_time_is_automatically_set_to_now(self):
        # timezone.now() uses UTC (not the timezone set in settings.py)
        # and django stores dates in UTC (the serializer does use timezone from settings.py)
        time_before_creation = timezone.now()
        simulation = LAWMSimulation.objects.create()
        time_after_creation = timezone.now()
        self.assertGreater(simulation.created, time_before_creation)
        self.assertGreater(time_after_creation, simulation.created)


class LAWMResultTest(TestCase):
    def test_all_attributes_are_readable_and_casted_to_variables(self):
        value = 423.32
        simulation = LAWMSimulation.objects.create()
        res = LAWMResult.objects.create(
            simulation=simulation,
            pop=value,
            popr=value,
        )
        self.assertEqual(res.pop, Population(value))
        self.assertEqual(res.popr, PopulationGrowth(value))

