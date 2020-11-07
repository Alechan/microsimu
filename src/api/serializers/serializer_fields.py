from rest_framework import serializers


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


class ParameterIntegerSerializerField(serializers.IntegerField):
    """
    Serializer field targeting custom ParameterIntegerField
    """

    def to_representation(self, value):
        """
        Convert the initial datatype into a primitive, serializable datatype.
        :param value: 
        :return: 
        """
        return int(value.value)
