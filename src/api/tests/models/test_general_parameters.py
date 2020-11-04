from django.test import TestCase

from api.models.models import GeneralParameters
from api.tests.api_test_mixin import ApiTestMixin


class LAWMGeneralParametersTest(TestCase, ApiTestMixin):
    def setUpTestData(cls):
        db_tree = cls.create_full_simulation_db_tree()
        cls.general_parameters = db_tree.general_parameters

    def test_default_values_are_set_when_none_provided(self):
        gen_params = GeneralParameters.objects.create()
        self.assertEqual(gen_params.KSTOP, 42)

    def test_default_values_can_be_overriden(self):
        gen_params = GeneralParameters.objects.create(KSTOP=2)
        self.assertEqual(gen_params.KSTOP, 2)

    def test_all_attributes_are_readable_and_casted_to_lawm_parameters(self):
        self.fail("hacer test en custom field para ParameterFloatField")
