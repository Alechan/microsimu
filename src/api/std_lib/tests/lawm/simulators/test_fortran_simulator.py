import shutil
import tempfile
from pathlib import Path

import pandas
from freezegun import freeze_time

from api.settings_api import LAWM_CSV_PER_REGION
from api.std_lib.lawm.general_parameters import SimulationStop
from api.std_lib.lawm.regions import Developed, Latinamerica, Africa, Asia
from api.std_lib.lawm.simulator.exceptions import ValidInputButSimulationError
from api.std_lib.lawm.simulator.fortran.lawm_fortran_simulator import LAWMFortranSimulator
from api.std_lib.tests.lawm.simulators.base_fortran_test import BaseFortranTest
from api.tests.helpers.general_asserts_mixin import GeneralAssertsMixin

YEAR = 2020
MONTH = 11
DAY = 10
HOUR = 16
MINUTE = 46
SECOND = 42
MICRO_SECOND = 342527

DATETIME_KWARGS = {
    "year"       : YEAR,
    "month"      : MONTH,
    "day"        : DAY,
    "hour"       : HOUR,
    "minute"     : MINUTE,
    "second"     : SECOND,
    "microsecond": MICRO_SECOND,
}


@freeze_time(f"{YEAR}-{MONTH}-{DAY} {HOUR}:{MINUTE}:{SECOND}")
class TestFortranSimulator(BaseFortranTest, GeneralAssertsMixin):
    @classmethod
    def setUpTestData(cls):
        # Create tempdir and save its path
        cls._temp_dir = Path(tempfile.mkdtemp())
        # Each test case can create individual files
        cls._temp_files = []
        cls.simulator = LAWMFortranSimulator(cls._temp_dir)
        cls.validated_data = cls.get_POST_parameters_example()
        cls.actual_dfs_per_region = cls.simulator.simulate(cls.validated_data)
        cls.expected_ts_dir = cls._temp_dir / "tmp" / f"{YEAR}-{MONTH}-{DAY}" / f"{HOUR}_{MINUTE}_{SECOND}"
        cls.expected_cfg_path = cls.expected_ts_dir / "run.cfg"
        cls.expected_developed_csv_path    = cls.expected_ts_dir / "result_reg_1_all.csv"
        cls.expected_latinamerica_csv_path = cls.expected_ts_dir / "result_reg_2_all.csv"
        cls.expected_africa_csv_path       = cls.expected_ts_dir / "result_reg_3_all.csv"
        cls.expected_asia_csv_path         = cls.expected_ts_dir / "result_reg_4_all.csv"
        cls.std_dev_path              = LAWM_CSV_PER_REGION[Developed.name]
        cls.std_latinamerica_csv_path = LAWM_CSV_PER_REGION[Latinamerica.name]
        cls.std_africa_csv_path       = LAWM_CSV_PER_REGION[Africa.name]
        cls.std_asia_csv_path         = LAWM_CSV_PER_REGION[Asia.name]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls._temp_dir)
        for f in cls._temp_files:
            f.close()
        super().tearDownClass()

    def test_assert_a_new_timestamp_dir_is_created(self):
        self.assertTrue(self.expected_ts_dir.is_dir())

    def test_assert_simulation_results_are_stored_in_new_timestamp_tmp(self):
        self.assertTrue(self.expected_cfg_path.is_file())

    def test_assert_csvs_are_created(self):
        self.assertTrue(self.expected_developed_csv_path    .is_file())
        self.assertTrue(self.expected_latinamerica_csv_path .is_file())
        self.assertTrue(self.expected_africa_csv_path       .is_file())
        self.assertTrue(self.expected_asia_csv_path         .is_file())

    def test_default_input_should_give_same_result_as_std_run(self):
        self.assert_files_equal(self.expected_developed_csv_path   , self.std_dev_path)
        self.assert_files_equal(self.expected_latinamerica_csv_path, self.std_latinamerica_csv_path)
        self.assert_files_equal(self.expected_africa_csv_path      , self.std_africa_csv_path)
        self.assert_files_equal(self.expected_asia_csv_path        , self.std_asia_csv_path)

    def test_the_dfs_returned_are_the_ones_from_the_csvs(self):
        expected_dev_df    = self.get_df(self.expected_developed_csv_path)
        expected_la_df     = self.get_df(self.expected_latinamerica_csv_path)
        expected_africa_df = self.get_df(self.expected_africa_csv_path)
        expected_asia_df   = self.get_df(self.expected_asia_csv_path)

        self.assert_dfs_equal(expected_dev_df    , self.actual_dfs_per_region[Developed.name])
        self.assert_dfs_equal(expected_la_df     , self.actual_dfs_per_region[Latinamerica.name])
        self.assert_dfs_equal(expected_africa_df , self.actual_dfs_per_region[Africa.name])
        self.assert_dfs_equal(expected_asia_df   , self.actual_dfs_per_region[Asia.name])

    def test_if_exec_returns_an_error_an_exception_is_raised(self):
        with tempfile.TemporaryDirectory() as new_temp_dir:
            new_temp_dir_path = Path(new_temp_dir)
            simulator = LAWMFortranSimulator(new_temp_dir_path)
            data = self.get_POST_parameters_example()
            # Change a parameter to one that results in an error simulation
            data["general_parameters"]["simulation_stop"] = SimulationStop(3000)
            try:
                _ = simulator.simulate(data)
                self.fail("An error should've been raises but wasn't.")
            except ValidInputButSimulationError:
                pass

    @staticmethod
    def get_df(csv_path):
        return pandas.read_csv(csv_path)
