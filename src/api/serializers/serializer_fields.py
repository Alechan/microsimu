from rest_framework import serializers

class MicroSimuSerializerField(serializers.ModelField):
    def to_representation(self, obj):
        """
        Convert the initial datatype into a primitive, serializable datatype.
        :param value:
        :return:
        """
        nondjangomodel_component_instance = self.model_field.value_from_object(obj)
        value = nondjangomodel_component_instance.value
        return value


class VariableFloatSerializerField(MicroSimuSerializerField):
    pass
# class VariableFloatSerializerField(serializers.Field):
# """
    # Serializer field targeting custom VariableFloatField
    # """
    #
    # def to_representation(self, value):
    #     return float(value.value)


class ParameterFloatSerializerField(MicroSimuSerializerField):
    pass
# class ParameterFloatSerializerField(serializers.Field):
#     """
#     Serializer field targeting custom ParameterFloatField
#     """
#
#     def to_internal_value(self, data):
#         assert False
#
#     def to_representation(self, value):
#         return float(value.value)

class ParameterIntegerSerializerField(MicroSimuSerializerField):
    pass
# class ParameterIntegerSerializerField(serializers.ModelField):
#     def to_representation(self, obj):
#         """
#         Convert the initial datatype into a primitive, serializable datatype.
#         :param value:
#         :return:
#         """
#         nondjangomodel_component_instance = self.model_field.value_from_object(obj)
#         value = nondjangomodel_component_instance.value
#         return value

# class ParameterIntegerSerializerField(serializers.IntegerField):
#     """
#     Serializer field targeting custom ParameterIntegerField
#     """
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     def to_representation(self, value):
#         """
#         Convert the initial datatype into a primitive, serializable datatype.
#         :param value:
#         :return:
#         """
#         return int(value.value)
