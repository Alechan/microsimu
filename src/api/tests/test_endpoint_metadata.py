from django.test import TestCase

from api.endpoint_metadata import DescriptiveFieldsMetadater
from api.serializers.parameters_serializers import RunParametersSerializer


class DescriptiveFieldsMetadataTest(TestCase):
    def setUp(self):
        self.serializer = RunParametersSerializer()
        self.metadater  = DescriptiveFieldsMetadater()

    def test_metadater_for_serializer_includes_expected_fields(self):
        expected_metadata = self.serializer.get_metadata()

        actual_metadata = self.metadater.get_serializer_info(self.serializer)

        self.assertEqual(expected_metadata, actual_metadata)

