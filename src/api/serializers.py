from urllib import request

from rest_framework import serializers
from django.urls import reverse

from api.models import fields
from api.models.models import LAWMSimulation, LAWMYearResult, LAWMRegionResult


class VariableFloatSerializerField(serializers.Field):
    """
    Serializer field targeting custom VariableFloatField
    """

    def to_representation(self, value):
        return float(value.value)


class ResultSerializerMetaClass(type(serializers.ModelSerializer)):
    """
    Metaclass to override class variables set in Django REST Framework ModelSerializer
    class.
    """
    def __new__(cls, clsname, bases, attrs):
        # noinspection PyTypeChecker
        super_new = super().__new__(cls, clsname, bases, attrs)
        super_new.serializer_field_mapping[fields.VariableFloatField] = VariableFloatSerializerField
        return super_new


class ResultSerializer(serializers.ModelSerializer, metaclass=ResultSerializerMetaClass):
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


class SimulationDetailSerializer(serializers.HyperlinkedModelSerializer):
    url     = serializers.HyperlinkedIdentityField(view_name="api:simulation-detail")
    regions = serializers.SerializerMethodField('get_regions_urls')

    def get_regions_urls(self, obj):
        request = self.context['request']
        regions_urls = {
            reg_res.region_name: self.get_url_from_region_result(reg_res, request)
            for reg_res in obj.region_results.all()
        }
        return regions_urls

    @staticmethod
    def get_url_from_region_result(reg_res, request):
        args = [reg_res.simulation_id, reg_res.region_name]
        relative_url = reverse("api:regionresult-detail", args=args)
        absolute_url = request.build_absolute_uri(relative_url)
        return absolute_url

    class Meta:
        model = LAWMSimulation
        fields = '__all__'


class SimulationListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:simulation-detail")

    class Meta:
        model = LAWMSimulation
        fields = ["url", "created"]
