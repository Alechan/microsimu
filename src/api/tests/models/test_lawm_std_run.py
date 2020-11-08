from django.test import TestCase

from api.models.models import LAWMSimulation
from api.tests.helpers.api_test_mixin import MicroSimuTestMixin


class LAWMStandardRunTest(TestCase, MicroSimuTestMixin):
    def test_first_simulation_corresponds_to_std_run(self):
        simus = LAWMSimulation.objects.filter(pk=1)

        self.assert_has_length(simus, 1)
        simu = simus[0]

        self.assert_simu_equivalent_to_std_run(simu)
