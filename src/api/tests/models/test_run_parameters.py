from django.test import TestCase

from api.tests.api_test_mixin import ApiTestMixin


class LAWMRunParametersTest(TestCase, ApiTestMixin):
    @classmethod
    def setUpTestData(cls):
        db_tree = cls.create_full_simulation_db_tree()
        cls.simu           = db_tree.simu
        cls.run_parameters = db_tree.run_parameters

    def test_simulation_returns_correct_object(self):
        expected_simu = self.simu
        actual_simu   = self.run_parameters.simulation
        self.assertEqual(expected_simu, actual_simu)

    def test_CAMBIAME_EL_NOMBRE(self):
        self.fail("Ver si faltan tests acá")



