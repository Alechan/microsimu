from rest_framework import serializers

from api.models.models import LAWMYearResult, LAWMRegionResult
from api.serializers.serializer_metaclass import MicroSimuSerializerMetaClass


class ResultSerializer(serializers.ModelSerializer, metaclass=MicroSimuSerializerMetaClass):
    """
    Serializes the instance's values into primitive types
    """

    class Meta:
        model = LAWMYearResult
        exclude = ["region_result", "id"]


class RegionResultSerializer(serializers.ModelSerializer):
    simulation = serializers.HyperlinkedRelatedField(view_name="api:simulation-detail", read_only=True)
    region     = serializers.ReadOnlyField(source='region.name')
    variables  = serializers.SerializerMethodField('get_variables_information')
    results    = ResultSerializer(many=True, read_only=True, source='year_results')

    # noinspection PyMethodMayBeStatic
    def get_variables_information(self, obj):
        vars_info = obj.get_variables_information()
        return vars_info

    class Meta:
        model = LAWMRegionResult
        exclude = ["id"]
