from rest_framework import serializers

from api.models import fields
from api.models.models import LAWMSimulation, LAWMResult


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
        model = LAWMResult
        exclude = ["simulation", "id"]


class SimulationDetailSerializer(serializers.ModelSerializer):
    results   = ResultSerializer(many=True, read_only=True)
    variables = serializers.SerializerMethodField('get_variables_information')

    # noinspection PyMethodMayBeStatic
    def get_variables_information(self, obj):
        vars_info = obj.get_variables_information()
        return vars_info

    class Meta:
        model = LAWMSimulation
        fields = '__all__'


class SimulationListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:simulation-detail")

    class Meta:
        model = LAWMSimulation
        fields = ["url", "created"]
