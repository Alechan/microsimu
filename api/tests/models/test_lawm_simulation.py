from django.test import TestCase
from django.utils import timezone

from api.models.models import LAWMSimulation, LAWMRegion, LAWMRegionResult
from api.tests.api_test_mixin import ApiTestMixin


class LAWMSimulationTest(TestCase, ApiTestMixin):
    @classmethod
    def setUpTestData(cls):
        db_tree = cls.create_full_simulation_db_tree()
        cls.simu = db_tree.simu
        cls.region_result_region_1 = db_tree.reg_res_s1_r1
        cls.region_result_region_2 = db_tree.reg_res_s1_r2

    def test_created_time_is_automatically_set_to_now(self):
        # *) timezone.now() uses UTC and not the timezone set in django's settings.py
        # *) django stores dates in UTC and the serializer uses the timezone from settings.py
        time_before_creation = timezone.now()
        simulation = LAWMSimulation.objects.create()
        time_after_creation = timezone.now()
        self.assertGreater(simulation.created, time_before_creation)
        self.assertGreater(time_after_creation, simulation.created)

    def test_regions_attribute_returns_correct_regions(self):
        actual_region_results = self.simu.region_results.all()

        expected_region_results = [self.region_result_region_1, self.region_result_region_2]

        self.assertEqual(len(actual_region_results), len(expected_region_results))
        self.assertEqual(expected_region_results[0], actual_region_results[0])
        self.assertEqual(expected_region_results[1], actual_region_results[1])
