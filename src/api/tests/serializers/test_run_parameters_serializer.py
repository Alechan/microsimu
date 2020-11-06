from django import test

from api.models.models import GeneralParameters, LAWMRunParameters
from api.serializers import RunParametersSerializer
from api.tests.api_test_mixin import ApiTestMixin


class RunParametersSerializerTest(test.TestCase, ApiTestMixin):
    @classmethod
    def setUpTestData(cls):
        db_tree = cls.create_full_simulation_db_tree()
        cls.simu           = db_tree.simu
        cls.run_parameters = db_tree.run_parameters
        serializer = RunParametersSerializer(cls.run_parameters)
        cls.data = serializer.data

    def test_uninitialized_serializer_returns_correct_fields_metadata(self):
        expected_metadata = LAWMRunParameters.get_metadata()

        uninitialized_serializer = RunParametersSerializer()
        actual_metadata = uninitialized_serializer.get_metadata()

        self.assert_dicts_equal(expected_metadata, actual_metadata)




