from rest_framework import serializers

from api.models import fields
from api.models.models import LAWMSimulation, LAWMResult


class VariableFloatField(serializers.Field):
    """
    Serializer field targeting custom VariableFloatField
    """
    def to_representation(self, value):
        return float(value.value)


class SimulationSerializer(serializers.ModelSerializer):
    results = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = LAWMSimulation
        fields = '__all__'


class ResultSerializerMetaClass(type(serializers.ModelSerializer)):
    """
    Metaclass to override class variables set in Django REST Framework ModelSerializer
    class.
    """
    def __new__(cls, clsname, bases, attrs):
        super_new = super().__new__(cls, clsname, bases, attrs)
        super_new.serializer_field_mapping[fields.VariableFloatField] = VariableFloatField
        return super_new


class ResultSerializer(serializers.ModelSerializer, metaclass=ResultSerializerMetaClass):

    class Meta:
        model = LAWMResult
        fields = '__all__'
