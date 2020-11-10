from django import test

from api.models.models import LAWMGeneralParameters
from api.serializers.parameters_serializers import GeneralParametersSerializer
from api.tests.helpers.api_test_mixin import MicroSimuTestMixin


class GeneralParametersSerializerTest(test.TestCase, MicroSimuTestMixin):
    def test_serializer_class_method_returns_correct_default_values_serialized(self):
        gen_params = LAWMGeneralParameters.new_with_defaults()
        expected_data = GeneralParametersSerializer(gen_params).data

        actual_data = GeneralParametersSerializer.get_default_serialized_data()

        self.assert_dicts_equal(expected_data, actual_data)
