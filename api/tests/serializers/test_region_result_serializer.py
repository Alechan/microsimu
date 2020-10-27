from django import test

from api.serializers import RegionResultSerializer
from api.std_lib.lawm.variables import Population
from api.tests.api_test_mixin import ApiTestMixin


class RegionResultSerializerTest(test.TestCase, ApiTestMixin):
    @classmethod
    def setUpTestData(cls):
        db_tree = cls.create_full_simulation_db_tree()
        cls.region_result = db_tree.region_result_r1
        serializer = RegionResultSerializer(cls.region_result, context={"request": None})
        cls.data = serializer.data

    def test_returns_correct_fields(self):
        expected_fields = {"simulation", "region", "results", "variables"}

        actual_fields = self.data.keys()
        self.assertEqual(expected_fields, actual_fields)

    def test_includes_region_name(self):
        self.assertEqual(self.data["region"], self.region_result.region_name)

    def test_serializer_returns_expanded_results(self):
        y_1960_values = self.get_year_result_creation_kwargs(self.region_result, year=1960)
        del y_1960_values["region_result"]

        y_1961_values = self.get_year_result_creation_kwargs(self.region_result, year=1961)
        del y_1961_values["region_result"]

        expected_results = [y_1960_values, y_1961_values]
        actual_results = self.data["results"]

        self.assertEqual(expected_results, actual_results)

    def test_serializer_returns_variables(self):
        variables = self.data["variables"]
        self.assertEqual(len(variables), 44)
        self.assertEqual(
            variables["pop"],
            Population.info_as_dict()
        )
