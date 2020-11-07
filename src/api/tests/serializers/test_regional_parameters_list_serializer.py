from django import test

from api.serializers import RegionalParametersSerializer, RegionalParametersManySerializer
from api.tests.api_test_mixin import MicroSimuTestMixin


class RegionalParametersListSerializerTest(test.TestCase, MicroSimuTestMixin):
    @classmethod
    def setUpTestData(cls):
        db_tree = cls.create_full_simulation_db_tree()
        cls.all_reg_params = db_tree.all_reg_params
        serializer = RegionalParametersSerializer(many=True)
        # I have to use the "to_representation" because when called in isolation with "many=True",
        # the data returned doesn't call "to_representation" but when used as a nested serializer,
        # it does call "to_representation"
        cls.data = serializer.to_representation(cls.all_reg_params)
        cls.expected_fields = {reg.region.name for reg in cls.all_reg_params}

    def test_returns_correct_fields(self):
        actual_fields = self.data.keys()
        self.assertEqual(self.expected_fields, actual_fields)

    def test_returns_correct_values_per_region(self):
        for reg_params in self.all_reg_params:
            region_name = reg_params.region.name
            individual_serializer_data = RegionalParametersSerializer(reg_params).data
            expected_data = dict(individual_serializer_data)
            del expected_data["region"]
            actual_data = self.data[region_name]
            self.assert_dicts_equal(expected_data, actual_data)

    def test_serializer_class_method_returns_correct_default_values_serialized(self):
        expected_data = self.data
        actual_data = RegionalParametersManySerializer.default_values_data()

        self.assert_dicts_equal(expected_data, actual_data)

