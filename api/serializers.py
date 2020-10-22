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
    results = ResultSerializer(many=True, read_only=True)

    class Meta:
        model = LAWMSimulation
        fields = '__all__'


class SimulationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LAWMSimulation
        fields = ["id", "created"]
