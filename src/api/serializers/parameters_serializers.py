from rest_framework import serializers

from api.models.models import LAWMGeneralParameters, LAWMRegionalParameters, \
    LAWMRunParameters
from api.serializers.serializer_metaclass import MicroSimuSerializerMetaClass


class GeneralParametersSerializer(serializers.ModelSerializer, metaclass=MicroSimuSerializerMetaClass):

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
        data_list = [value | {"region": key} for key, value in data.items()]
        return super().to_internal_value(data_list)


class RegionalParametersSerializer(serializers.ModelSerializer, metaclass=MicroSimuSerializerMetaClass):
    class Meta:
        model = LAWMRegionalParameters
        exclude = ["id", "run_parameters"]
        list_serializer_class = ManyRegionalParametersSerializer


class RunParametersSerializer(serializers.ModelSerializer, metaclass=MicroSimuSerializerMetaClass):
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
