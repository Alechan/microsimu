from collections import OrderedDict

from rest_framework.metadata import SimpleMetadata


class DescriptiveFieldsMetadater(SimpleMetadata):
    def get_serializer_info(self, serializer):
        """
        Given an instance of a serializer return a dictionary
        of metadata about it.
        """
        serializer_metadata = serializer.get_metadata()
        return serializer_metadata

