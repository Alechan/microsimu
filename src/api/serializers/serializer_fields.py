from rest_framework import serializers


class MicroSimuSerializerFieldMixin:
    def __init__(self, *args, **kwargs):
        # Force all serializer fields to be required for now
        kwargs["required"] = True
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        """
        Use the Django Model field to go from primitive data type (int, float, list) to
        python object (SimulationStop(2000), MaxCalories(3200))
        :param data:
        :return:
        """
        django_model = self.parent.Meta.model
        django_field_name = self.source
        django_field_descriptor = getattr(django_model, django_field_name)
        django_field = django_field_descriptor.field
        return django_field.to_python(data)

    def to_representation(self, obj):
        """
        Convert the initial datatype into a primitive, serializable datatype.
        :param value:
        :return:
        """
        nondjangomodel_component_instance = self.model_field.value_from_object(obj)
        value = nondjangomodel_component_instance.value
        return value


class VariableFloatSerializerField(MicroSimuSerializerFieldMixin, serializers.FloatField):
    """
    Serializer field targeting custom VariableFloatField
    """

    def to_representation(self, value):
        return float(value.value)


class ParameterFloatSerializerField(MicroSimuSerializerFieldMixin, serializers.FloatField):
    """
    Serializer field targeting custom ParameterFloatField
    """
    def to_representation(self, value):
        """
        Convert the initial datatype into a primitive, serializable datatype.
        :param value:
        :return:
        """
        return float(value.value)


class ParameterIntegerSerializerField(MicroSimuSerializerFieldMixin, serializers.IntegerField):
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

