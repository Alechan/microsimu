from api.std_lib.lawm.simulator.fortran.lawm_fortran_simulator import LAWMFortranSimulator
from api.std_lib.tests.lawm.simulators.base_fortran_test import BaseFortranTest
from api.tests.helpers.general_asserts_mixin import GeneralAssertsMixin


class TestFortranSimulator(BaseFortranTest, GeneralAssertsMixin):
    def test_default_input_should_give_same_result_as_std_run(self):
        simulator  = LAWMFortranSimulator()
        dfs_per_region = simulator.simulate()
