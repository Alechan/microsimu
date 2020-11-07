from django.urls import reverse
from rest_framework import serializers

from api.models import fields
from api.models.models import LAWMSimulation, LAWMYearResult, LAWMRegionResult, LAWMGeneralParameters, LAWMRegionalParameters, \
    LAWMRunParameters


class VariableFloatSerializerField(serializers.Field):
    """
    Serializer field targeting custom VariableFloatField
    """

    def to_representation(self, value):
        return float(value.value)


class ParameterFloatSerializerField(serializers.Field):
    """
    Serializer field targeting custom ParameterFloatField
    """

    def to_representation(self, value):
        return float(value.value)


class ParameterIntegerSerializerField(serializers.Field):
    """
    Serializer field targeting custom ParameterFloatField
    """

    def to_representation(self, value):
        return int(value.value)


class ResultSerializerMetaClass(type(serializers.ModelSerializer)):
    """
    Metaclass to override class variables set in Django REST Framework ModelSerializer
    class.
    """
    def __new__(cls, clsname, bases, attrs):
        # noinspection PyTypeChecker
        super_new = super().__new__(cls, clsname, bases, attrs)
        super_new.serializer_field_mapping[fields.VariableFloatField]    = VariableFloatSerializerField
        super_new.serializer_field_mapping[fields.ParameterFloatField]   = ParameterFloatSerializerField
        super_new.serializer_field_mapping[fields.ParameterIntegerField] = ParameterIntegerSerializerField
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


class GeneralParametersSerializer(serializers.ModelSerializer, metaclass=ResultSerializerMetaClass):

    @classmethod
    def get_default_serialized_data(cls):
        default_values = LAWMGeneralParameters.new_with_defaults()
        serializer = GeneralParametersSerializer(default_values)
        return serializer.data

    class Meta:
        model = LAWMGeneralParameters
        exclude = ["id"]


class ManyRegionalParametersSerializer(serializers.ListSerializer):
    """
    Serializes to a dict of {region:data-region} instead of a list of [data]
    """
    @classmethod
    def get_default_serialized_data(cls):
        reg_params_per_region = LAWMRegionalParameters.new_in_memory_with_defaults_all_regions()
        all_reg_params        = reg_params_per_region.values()
        serializer = RegionalParametersSerializer(many=True)
        # I have to use the "to_representation" because when called in isolation with "many=True",
        # the data returned doesn't call "to_representation" but when used as a nested serializer,
        # it does call "to_representation"
        data = serializer.to_representation(all_reg_params)
        return data

    def to_representation(self, data):
        """
        From python objects to primitive types (int, float, dict, list)
        (the inverse of to_internal_value)
        :param data: the python objects
        :return: a dictionary of primitive types
        """
        data_list = super().to_representation(data)
        data_dict = {}
        for reg_params in data_list:
            region_name = reg_params["region"]
            params = reg_params.copy()
            del params["region"]
            data_dict[region_name] = params
        return data_dict

    def to_internal_value(self, data):
        """
        From  primitive types (int, float, dict, list) to python objects
        (the inverse of to_representation)
        :param data: a dictionary of primitive types
        :return: the python objects
        """
        data_list = [value | {"region":key} for key, value in data.items()]
        return super().to_internal_value(data_list)


class RegionalParametersSerializer(serializers.ModelSerializer, metaclass=ResultSerializerMetaClass):
    class Meta:
        model = LAWMRegionalParameters
        exclude = ["id", "run_parameters"]
        list_serializer_class = ManyRegionalParametersSerializer


class RunParametersSerializer(serializers.ModelSerializer, metaclass=ResultSerializerMetaClass):
    general  = GeneralParametersSerializer(source="general_parameters")
    regional = RegionalParametersSerializer(many=True, source="regional_parameters")

    class Meta:
        model = LAWMRunParameters
        exclude = ["id", "general_parameters", "simulation"]

    @property
    def data(self):
        """
        Hack to "force" the initial data shown in the HTML "free type form"
        :return:
        """
        if not self.instance:
            data = self.get_default_serialized_data()
        else:
            data = super().data
        return data

    @classmethod
    def get_default_serialized_data(cls):
        return {
            "general" : GeneralParametersSerializer.get_default_serialized_data(),
            "regional": ManyRegionalParametersSerializer.get_default_serialized_data(),
        }

    def create(self, validated_data):
        """
        Override creation because we have nested serializers and DRF can't handle automatic creation
        in this case.

        :param validated_data: a dict of validated data to be used to initialize Django model objects
        :return:
        """
        general_parameters = LAWMGeneralParameters.objects.create(**validated_data["general_parameters"])
        run_parameters = LAWMRunParameters.objects.create(general_parameters=general_parameters)
        for reg_params in validated_data["regional_parameters"]:
            regional_parameters = LAWMRegionalParameters.objects.create(
                run_parameters=run_parameters,
                **reg_params
            )
        return run_parameters

    def get_metadata(self):
        """
        Get fields metadata to inform the user about their defaults, max, min, etc
        :return:
        """
        return self.Meta.model.get_metadata()
