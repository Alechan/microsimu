from django.core.exceptions import ValidationError
from django.test import TestCase

from api.models.models import LAWMRegionalParameters, LAWMRunParameters, LAWMRegion
from api.std_lib.lawm.regional_parameters import *
from api.std_lib.lawm.regions import Developed
from api.tests.api_test_mixin import MicroSimuTestMixin, DEFAULT_REGIONS


class RegionalParametersTest(TestCase, MicroSimuTestMixin):
    def test_new_in_memory_objects_for_all_doesnt_modify_the_db(self):
        expected_db_reg_params_per_region = LAWMRegionalParameters.objects.all()

        _ = LAWMRegionalParameters.new_in_memory_with_defaults_all_regions()

        actual_db_reg_params_per_region = LAWMRegionalParameters.objects.all()

        self.assert_have_equal_length(expected_db_reg_params_per_region, actual_db_reg_params_per_region)
        for first_obj, second_obj in zip(expected_db_reg_params_per_region, actual_db_reg_params_per_region):
            self.assertEqual(first_obj, second_obj)

    def test_new_in_memory_objects_for_all_regions_works(self):
        expected_developed_defaults, _, _ = self.get_developed_region_defaults()

        actual_reg_params_per_region = LAWMRegionalParameters.new_in_memory_with_defaults_all_regions()

        actual_regions = actual_reg_params_per_region.keys()
        self.assert_has_length(actual_regions, len(DEFAULT_REGIONS))
        actual_developed_defaults = actual_reg_params_per_region[Developed.name]
        self.assert_equal_in_memory_django_models(expected_developed_defaults, actual_developed_defaults)

    def test_create_instance_with_defaults_for_region_works(self):
        dev_defaults, region, run_parameters = self.get_developed_region_defaults()

        self.assertEqual(dev_defaults.run_parameters          , run_parameters)
        self.assertEqual(dev_defaults.region                  , region)
        self.assertEqual(dev_defaults.max_calories            , MaxCalories                    (3200 ))
        self.assertEqual(dev_defaults.max_build_cost          , MaxBuildCost                   (10   ))
        self.assertEqual(dev_defaults.tech_prog_coeff_1       , TechProgressCoefficient1       (1.01 ))
        self.assertEqual(dev_defaults.tech_prog_coeff_2       , TechProgressCoefficient2       (1.01 ))
        self.assertEqual(dev_defaults.tech_prog_coeff_3       , TechProgressCoefficient3       (1.005))
        self.assertEqual(dev_defaults.tech_prog_coeff_4       , TechProgressCoefficient4       (1.01 ))
        self.assertEqual(dev_defaults.tech_prog_coeff_5       , TechProgressCoefficient5       (1.015))
        self.assertEqual(dev_defaults.tech_prog_stop          , TechProgressStop               (3000 ))
        self.assertEqual(dev_defaults.years_building_cost_eq  , YearsForBuildingCostEquality   (40   ))
        self.assertEqual(dev_defaults.years_housing_level_eq  , YearsForHousingLevelEquality   (10    ))
        self.assertEqual(dev_defaults.desired_food_stock      , DesiredFoodStock               (365  ))
        self.assertEqual(dev_defaults.years_space_p_person_eq , YearsForSpacePerPersonEquality (40   ))
        self.assertEqual(dev_defaults.max_space_p_person      , MaxSpacePerPerson              (30   ))
        self.assertEqual(dev_defaults.desired_space_p_person  , DesiredSpacePerPerson          (30   ))
        self.assertEqual(dev_defaults.max_sec_5_gnp_propor    , MaxCapitalGoodsGNPProportion   (0.25 ))

    def get_developed_region_defaults(self):
        run_parameters = LAWMRunParameters()
        region = LAWMRegion(name="developed")
        dev_defaults = LAWMRegionalParameters.new_with_defaults_for_region(run_parameters, region)
        return dev_defaults, region, run_parameters

    def test_validators_are_automatically_added(self):
        expected_max_calories_error_message = 'Ensure this value is less than or equal to 3200.0.'

        overflowed_max_calories_creation_kwargs = self.get_creation_kwargs_with_overflowed_max_calories()

        gen_params = LAWMRegionalParameters(**overflowed_max_calories_creation_kwargs)
        try:
            gen_params.full_clean()
            self.fail("An error should've been raised but wasn't.")
        except ValidationError as e:
            actual_error_dict = e.error_dict
            expected_error_keys = {"max_calories"}
            actual_error_keys = actual_error_dict.keys()
            self.assertEqual(expected_error_keys, actual_error_keys)
            actual_max_calories_errors = actual_error_dict["max_calories"]
            self.assert_has_length(actual_max_calories_errors, 1)
            actual_max_calories_error_messages = actual_max_calories_errors[0].messages
            self.assert_has_length(actual_max_calories_error_messages, 1)
            actual_error_message   = actual_max_calories_error_messages[0]
            self.assertEqual(expected_max_calories_error_message, actual_error_message)

    def test_get_metadata_returns_correct_information(self):
        expected_metadata = {
            "max_calories"           : MaxCalories.info_as_dict(),
            "max_build_cost"         : MaxBuildCost.info_as_dict(),
            "tech_prog_coeff_1"      : TechProgressCoefficient1.info_as_dict(),
            "tech_prog_coeff_2"      : TechProgressCoefficient2.info_as_dict(),
            "tech_prog_coeff_3"      : TechProgressCoefficient3.info_as_dict(),
            "tech_prog_coeff_4"      : TechProgressCoefficient4.info_as_dict(),
            "tech_prog_coeff_5"      : TechProgressCoefficient5.info_as_dict(),
            "tech_prog_stop"         : TechProgressStop.info_as_dict(),
            "years_building_cost_eq" : YearsForBuildingCostEquality.info_as_dict(),
            "years_housing_level_eq" : YearsForHousingLevelEquality.info_as_dict(),
            "desired_food_stock"     : DesiredFoodStock.info_as_dict(),
            "years_space_p_person_eq": YearsForSpacePerPersonEquality.info_as_dict(),
            "max_space_p_person"     : MaxSpacePerPerson.info_as_dict(),
            "desired_space_p_person" : DesiredSpacePerPerson.info_as_dict(),
            "max_sec_5_gnp_propor"   : MaxCapitalGoodsGNPProportion.info_as_dict(),
        }
        actual_metadata = LAWMRegionalParameters.get_metadata()

        self.assertEqual(expected_metadata, actual_metadata)

    @staticmethod
    def get_creation_kwargs_with_overflowed_max_calories():
        run_parameters = LAWMRunParameters()
        # Uses the standard run region so depends on it
        region = LAWMRegion(name="developed")
        partial_creation_kwargs = LAWMRegionalParameters.get_default_values_for_region(region.name)
        partial_creation_kwargs["max_calories"] = 99999

        creation_kwargs = partial_creation_kwargs.copy()
        creation_kwargs["run_parameters"] = run_parameters
        creation_kwargs["region"] = region
        return creation_kwargs
