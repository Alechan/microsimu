from django import test

from api.models.models import LAWMRegionalParameters
from api.serializers.parameters_serializers import RegionalParametersSerializer
from api.tests.helpers.api_test_mixin import MicroSimuTestMixin


class RegionalParametersSerializerTest(test.TestCase, MicroSimuTestMixin):
    @classmethod
    def setUpTestData(cls):
        db_tree = cls.create_full_simulation_db_tree()
        cls.reg_params_developed = db_tree.regional_parameters_developed
        serializer = RegionalParametersSerializer(cls.reg_params_developed)
        cls.data = serializer.data
        all_fields = {field.name for field in LAWMRegionalParameters._meta.get_fields()}
        cls.expected_fields = all_fields - {"id", "run_parameters"}

    def test_returns_correct_fields(self):
        actual_fields = self.data.keys()
        self.assertEqual(self.expected_fields, actual_fields)

    def test_returns_correct_value_for_region(self):
        python_field_value = self.reg_params_developed.region
        expected_value = python_field_value.name
        actual_value = self.data["region"]
        self.assertEqual(expected_value, actual_value)

    def test_returns_correct_values_for_all_but_region(self):
        for field_name in self.expected_fields - {"region"}:
            python_field_value = getattr(self.reg_params_developed, field_name)
            expected_value = python_field_value.value
            actual_value   = self.data[field_name]
            self.assertEqual(expected_value, actual_value)
