from django import test

from api.models.models import LAWMGeneralParameters, LAWMRunParameters, LAWMRegionalParameters, LAWMSimulation
from api.serializers import RunParametersSerializer, GeneralParametersSerializer, RegionalParametersSerializer, \
    ManyRegionalParametersSerializer
from api.tests.api_test_mixin import MicroSimuTestMixin


class RunParametersSerializerTest(test.TestCase, MicroSimuTestMixin):
    @classmethod
    def setUpTestData(cls):
        db_tree = cls.create_full_simulation_db_tree()
        cls.simu           = db_tree.simu
        cls.run_parameters = db_tree.run_parameters
        serializer = RunParametersSerializer(cls.run_parameters)
        cls.data = serializer.data

    def test_when_instance_is_provided_the_data_returned_should_be_correct(self):
        value = 2323
        simu = LAWMSimulation.objects.create()
        general_parameters = LAWMGeneralParameters.objects.create(simulation_stop=value)
        run_parameters = LAWMRunParameters.objects.create(simulation=simu, general_parameters=general_parameters)

        expected_gen_params_data = GeneralParametersSerializer.get_default_serialized_data()
        expected_gen_params_data["simulation_stop"] = value

        expected_run_params_data = {
            "general": expected_gen_params_data,
            "regional": {}
        }

        actual_run_params_data = RunParametersSerializer(run_parameters).data

        self.assert_dicts_equal(expected_run_params_data, actual_run_params_data)

    def test_serializer_is_initialized_with_default_data_when_none_provided(self):
        expected_run_params_data = RunParametersSerializer.get_default_serialized_data()

        actual_run_params_data = RunParametersSerializer().data

        self.assert_dicts_equal(expected_run_params_data, actual_run_params_data)

    def test_serializer_class_method_returns_correct_default_values_serialized(self):
        expected_run_params_data = {
            "general" : GeneralParametersSerializer.get_default_serialized_data(),
            "regional": ManyRegionalParametersSerializer.get_default_serialized_data(),
        }

        actual_run_params_data = RunParametersSerializer.get_default_serialized_data()

        self.assert_dicts_equal(expected_run_params_data, actual_run_params_data)

    @staticmethod
    def get_expected_serialized_data_for_regional_params(db_regions, run_parameters):
        expected_reg_params_data = {}
        for reg in db_regions:
            reg_params = LAWMRegionalParameters.new_with_defaults_for_region(run_parameters, reg)
            reg_params_data = RegionalParametersSerializer(reg_params).data
            del reg_params_data["region"]
            region_name = reg.name
            expected_reg_params_data[region_name] = reg_params_data
        return expected_reg_params_data

    @staticmethod
    def get_serialized_data_for_general_params():
        gen_params = LAWMGeneralParameters.new_with_defaults()
        expected_gen_params_data = GeneralParametersSerializer(gen_params).data
        return expected_gen_params_data

    def test_uninitialized_serializer_returns_correct_fields_metadata(self):
        expected_metadata = LAWMRunParameters.get_metadata()

        uninitialized_serializer = RunParametersSerializer()
        actual_metadata = uninitialized_serializer.get_metadata()

        self.assert_dicts_equal(expected_metadata, actual_metadata)




