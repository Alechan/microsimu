from django.test import TestCase

from api.models.models import GeneralParameters
from api.tests.api_test_mixin import ApiTestMixin


class LAWMRegionalParametersYearResultTest(TestCase, ApiTestMixin):
    def test_default_values_are_set_when_none_provided(self):
        self.fail("adaptar a regional parameters")
        gen_params = GeneralParameters.objects.create()
        self.assertEqual(gen_params.KSTOP, 42)
