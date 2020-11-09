from api.models.models import LAWMRegion, MaxCalories, OptimizationStart
from api.std_lib.lawm.general_parameters import SimulationStop, WeightConstraint1, WeightConstraint2, WeightConstraint3
from api.std_lib.lawm.regional_parameters import TechProgressCoefficient1, TechProgressCoefficient2
from api.std_lib.lawm.simulator.fortran.lawm_fortran_cfg_formatter import LAWMFortranCFGFormatter
from api.std_lib.tests.lawm.simulators.base_fortran_test import BaseFortranTest
from api.tests.helpers.general_asserts_mixin import GeneralAssertsMixin


class LAWMFortranCFGFormatterTest(BaseFortranTest, GeneralAssertsMixin):
    def setUp(self):
        self.cfg_formatter = LAWMFortranCFGFormatter()

    def test_flatten_general_params_lvl_1_returns_correct_object(self):
        input_dict = {
            "general_parameters": {
                "simulation_stop"    : SimulationStop(2003),
                "optimization_start" : OptimizationStart(1980),
                "weight_constraint_1": WeightConstraint1(2.1),
                "weight_constraint_2": WeightConstraint2(2.2),
                "weight_constraint_3": WeightConstraint3(2.3),
            },
        }
        expected_flattened_dict = {
            "KSTOP": 2003,
            "KPROJ": 1980,
            "WTH(1)": 2.1,
            "WTH(2)": 2.2,
            "WTH(3)": 2.3,
        }
        actual_flattened_dict = self.cfg_formatter.flatten_general_params_lvl_1(input_dict)

        self.assert_dicts_equal(expected_flattened_dict, actual_flattened_dict)

    def test_flatten_general_params_lvl_2_returns_correct_object(self):
        input_dict = {
            "KSTOP"  : 2003,
            "KPROJ"  : 1980,
            "WTH(1)" : 2.01,
            "WTH(2)" : 2.02,
            "WTH(3)" : 2.03,
            "WTH(4)" : 2.04,
            "WTH(5)" : 2.05,
            "WTH(6)" : 2.06,
            "WTH(7)" : 2.07,
            "WTH(8)" : 2.08,
            "WTH(9)" : 2.09,
            "WTH(10)": 2.10,
            "WTH(11)": 2.11,
            "WTH(12)": 2.12,
            "WTH(13)": 2.13,
            "WTH(14)": 2.14,
            "WTH(15)": 2.15,
            "WTH(16)": 2.16,
            "WTH(17)": 2.17,
            "WTH(18)": 2.18,
            "WTH(19)": 2.19,
            "WTH(20)": 2.20,
            "WTH(21)": 2.21,
            "WTH(22)": 2.22,
            "WTH(23)": 2.23,
            "WTH(24)": 2.24,
            "WTH(25)": 2.25,
            "WTH(26)": 2.26,
        }
        expected_flattened_dict = {
            "KSTOP": 2003,
            "KPROJ": 1980,
            "WTH": [2.01, 2.02, 2.03, 2.04, 2.05,
                    2.06, 2.07, 2.08, 2.09, 2.10,
                    2.11, 2.12, 2.13, 2.14, 2.15,
                    2.16, 2.17, 2.18, 2.19, 2.20,
                    2.21, 2.22, 2.23, 2.24, 2.25,
                    2.26, -1  , -1  , -1  , -1]
        }
        actual_flattened_dict = self.cfg_formatter.flatten_general_params_lvl_2(input_dict)

        self.assert_dicts_equal(expected_flattened_dict, actual_flattened_dict)

    def test_flatten_regional_params_lvl_1_returns_correct_object(self):
        input_dict = {
            "regional_parameters": [
                {
                    "max_calories": MaxCalories(3203),
                    "tech_prog_coeff_1": TechProgressCoefficient1(1.01),
                    "tech_prog_coeff_2": TechProgressCoefficient2(1.02),
                    "region": LAWMRegion("developed")
                },
                {
                    "max_calories": MaxCalories(3231),
                    "tech_prog_coeff_1": TechProgressCoefficient1(1.03),
                    "tech_prog_coeff_2": TechProgressCoefficient2(1.04),
                    "region": LAWMRegion("latinamerica")
                },
            ]
        }
        expected_flattened_dict = {
            "CALMX(IB)"  : {"developed": 3203, "latinamerica": 3231},
            "GAMMA(IB,1)": {"developed": 1.01, "latinamerica": 1.03},
            "GAMMA(IB,2)": {"developed": 1.02, "latinamerica": 1.04},
        }
        actual_flattened_dict = self.cfg_formatter.flatten_regional_params_lvl_1(input_dict)

        self.assert_dicts_equal(expected_flattened_dict, actual_flattened_dict)

    def test_flatten_regional_params_lvl_2_returns_correct_object(self):
        input_dict = {
            "CALMX(IB)"  : {"developed": 2901, "latinamerica": 2902, "africa": 2903, "asia": 2904},
            "GAMMA(IB,1)": {"developed": 1.01, "latinamerica": 1.11, "africa": 1.21, "asia": 1.31},
            "GAMMA(IB,2)": {"developed": 1.02, "latinamerica": 1.12, "africa": 1.22, "asia": 1.32},
            "GAMMA(IB,3)": {"developed": 1.03, "latinamerica": 1.13, "africa": 1.23, "asia": 1.33},
            "GAMMA(IB,4)": {"developed": 1.04, "latinamerica": 1.14, "africa": 1.24, "asia": 1.34},
            "GAMMA(IB,5)": {"developed": 1.05, "latinamerica": 1.15, "africa": 1.25, "asia": 1.35},
        }
        expected_flattened_dict = {
            "CALMX": [2901, 2902, 2903, 2904],
            "GAMMA": [
                [1.01, 1.02, 1.03, 1.04, 1.05],
                [1.11, 1.12, 1.13, 1.14, 1.15],
                [1.21, 1.22, 1.23, 1.24, 1.25],
                [1.31, 1.32, 1.33, 1.34, 1.35],
            ]
        }
        actual_flattened_dict = self.cfg_formatter.flatten_regional_params_lvl_2(input_dict)

        self.assert_dicts_equal(expected_flattened_dict, actual_flattened_dict)

    def test_to_final_str_for_flatted_dict_returns_valid_string(self):
        general_params_flattened_dict = {
            "KSTOP": 2003,
            "KPROJ": 1980,
            "WTH": [2.01, 2.02, 2.03, 2.04, 2.05,
                    2.06, 2.07, 2.08, 2.09, 2.10,
                    2.11, 2.12, 2.13, 2.14, 2.15,
                    2.16, 2.17, 2.18, 2.19, 2.20,
                    2.21, 2.22, 2.23, 2.24, 2.25,
                    2.26, -1, -1, -1, -1]
        }
        regional_params_flattened_dict = {
            "CALMX": [2901, 2902, 2903, 2904],
            "GAMMA": [
                [1.01, 1.02, 1.03, 1.04, 1.05],
                [1.11, 1.12, 1.13, 1.14, 1.15],
                [1.21, 1.22, 1.23, 1.24, 1.25],
                [1.31, 1.32, 1.33, 1.34, 1.35],
            ]
        }
        input_dict = general_params_flattened_dict | regional_params_flattened_dict

        expected_str = \
"""CALMX
2901 2902 2903 2904
GAMMA
1.01 1.02 1.03 1.04 1.05
1.11 1.12 1.13 1.14 1.15
1.21 1.22 1.23 1.24 1.25
1.31 1.32 1.33 1.34 1.35
KPROJ
1980
KSTOP
2003
WTH
2.01 2.02 2.03 2.04 2.05
2.06 2.07 2.08 2.09 2.1
2.11 2.12 2.13 2.14 2.15
2.16 2.17 2.18 2.19 2.2
2.21 2.22 2.23 2.24 2.25
2.26 -1 -1 -1 -1
"""
        actual_str = self.cfg_formatter.to_final_str(input_dict)

        self.assertEqual(expected_str, actual_str)

    def test_given_valid_run_parameters_returns_correct_cfg_content(self):

        actual_cfg_content = self.cfg_formatter.cfg_content_from_validated_data(self.validated_data)

        self.assertEqual(self.expected_cfg_content, actual_cfg_content)

