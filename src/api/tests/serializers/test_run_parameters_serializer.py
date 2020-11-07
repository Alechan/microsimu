from django import test

from api.models.models import GeneralParameters, LAWMRunParameters, LAWMRegion, RegionalParameters
from api.serializers import RunParametersSerializer, GeneralParametersSerializer, RegionalParametersSerializer
from api.std_lib.lawm.regions import DEFAULT_REGIONS
from api.tests.api_test_mixin import MicroSimuTestMixin


class RunParametersSerializerTest(test.TestCase, MicroSimuTestMixin):
    @classmethod
    def setUpTestData(cls):
        db_tree = cls.create_full_simulation_db_tree()
        cls.simu           = db_tree.simu
        cls.run_parameters = db_tree.run_parameters
        serializer = RunParametersSerializer(cls.run_parameters)
        cls.data = serializer.data

    def test_serializer_class_method_returns_correct_default_values_serialized(self):
        # expected_gen_params_data = self.get_serialized_data_for_general_params()
        # db_regions = [LAWMRegion(name=reg.name) for reg in DEFAULT_REGIONS]
        # run_parameters = LAWMRunParameters()
        # expected_reg_params_data = self.get_expected_serialized_data_for_regional_params(db_regions, run_parameters)
        # expected_run_params_data = {
        #     "general" : expected_gen_params_data,
        #     "regional": expected_reg_params_data,
        # }

        actual_run_params_data = RunParametersSerializer.default_values_data()

        # self.assert_dicts_equal(expected_run_params_data, actual_run_params_data)

        # actual_run_params_data = LAWMRunParameters.as_dict_with_defaults()
        #
        # actual_run_params = LAWMRunParameters.as_dict_with_defaults()
        # actual_gen_params = actual_run_params.general_parameters
        # actual_reg_params = list(actual_run_params.regional_parameters.all())
        #
        # self.assert_have_equal_length(expected_reg_params, actual_reg_params)
        # for expected_reg, actual_reg in zip(expected_reg_params, actual_reg_params):
        #     self.assert_equal_in_memory_django_models(expected_reg, actual_reg)
        #
        # expected_metadata = LAWMRunParameters.get_metadata()
        #
        # uninitialized_serializer = RunParametersSerializer()
        # actual_metadata = uninitialized_serializer.get_metadata()
        #
        # self.assert_dicts_equal(expected_metadata, actual_metadata)

    @staticmethod
    def get_expected_serialized_data_for_regional_params(db_regions, run_parameters):
        expected_reg_params_data = {}
        for reg in db_regions:
            reg_params = RegionalParameters.new_with_defaults_for_region(run_parameters, reg)
            reg_params_data = RegionalParametersSerializer(reg_params).data
            del reg_params_data["region"]
            region_name = reg.name
            expected_reg_params_data[region_name] = reg_params_data
        return expected_reg_params_data

    @staticmethod
    def get_serialized_data_for_general_params():
        gen_params = GeneralParameters.new_with_defaults()
        expected_gen_params_data = GeneralParametersSerializer(gen_params).data
        return expected_gen_params_data

    def test_uninitialized_serializer_returns_correct_fields_metadata(self):
        expected_metadata = LAWMRunParameters.get_metadata()

        uninitialized_serializer = RunParametersSerializer()
        actual_metadata = uninitialized_serializer.get_metadata()

        self.assert_dicts_equal(expected_metadata, actual_metadata)




