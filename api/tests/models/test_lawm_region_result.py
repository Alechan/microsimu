from unittest import mock
from unittest.mock import MagicMock

import django
from django.test import TestCase

from api.models.models import LAWMRegionResult
from api.tests.api_test_mixin import ApiTestMixin


class LAWMRegionResultTest(TestCase, ApiTestMixin):
    @classmethod
    def setUpTestData(cls):
        db_tree = cls.create_full_simulation_db_tree()
        cls.simu   = db_tree.simu
        cls.region_1  = db_tree.region_1
        cls.region_result_region_1 = db_tree.reg_res_s1_r1
        cls.region_result_region_2 = db_tree.reg_res_s1_r2
        cls.year_results_reg_1 = db_tree.year_results_reg_1
        cls.year_results_reg_2 = db_tree.year_results_reg_2

    def test_unique_together_simu_and_region(self):
        try:
            _ = LAWMRegionResult.objects.create(simulation=self.simu, region=self.region_1)
            self.fail("Creating 2 region results with same region and simulation should raise an error.")
        except django.db.utils.IntegrityError:
            pass

    def test_returns_correct_region_name(self):
        self.assertEqual(self.region_1.name, self.region_result_region_1.region_name)

    def test_returns_correct_simulation_id(self):
        self.assertEqual(self.simu.id, self.region_result_region_1.simulation_id)

    def test_results_attributes_returns_correct_objects(self):

        self.assertEqual(self.region_result_region_1.simulation, self.simu)
        actual_results_1 = self.region_result_region_1.year_results.all()
        self.assertEqual(self.year_results_reg_1[0], actual_results_1[0])
        self.assertEqual(self.year_results_reg_1[1], actual_results_1[1])

        self.assertEqual(self.region_result_region_2.simulation, self.simu)
        actual_results_2 = self.region_result_region_2.year_results.all()
        self.assertEqual(self.year_results_reg_2[0], actual_results_2[0])
        self.assertEqual(self.year_results_reg_2[1], actual_results_2[1])

    @mock.patch('api.models.models.LAWMYearResult.get_variables_information')
    def test_get_variables_information_returns_results_variables_information_and_is_cached(self, method_mock):
        # Clean cache just in case other tests have set it up
        if hasattr(LAWMRegionResult, "_cached_vars_info"):
            del LAWMRegionResult._cached_vars_info

        vars_info_mock = MagicMock()
        method_mock.return_value = vars_info_mock

        # The first call should call the method
        self.assertEqual(method_mock.call_count, 0)
        region_result_1_vars_info   = self.region_result_region_1.get_variables_information()
        self.assertEqual(method_mock.call_count, 1)
        self.assertEqual(vars_info_mock, region_result_1_vars_info)

        # The second call to same object should NOT call the method
        region_result_1_vars_info_2   = self.region_result_region_1.get_variables_information()
        self.assertEqual(method_mock.call_count, 1)
        self.assertEqual(vars_info_mock, region_result_1_vars_info_2)

        # A third call but to another object should NOT call the method
        region_result_2_vars_info   = self.region_result_region_2.get_variables_information()
        self.assertEqual(method_mock.call_count, 1)
        self.assertEqual(vars_info_mock, region_result_2_vars_info)

        # Clean up cache or other tests will fail because it's stored in the model class (which is used
        # in all tests)
        del LAWMRegionResult._cached_vars_info


