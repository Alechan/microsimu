from api.models import fields
from api.serializers.serializer_fields import *


class MicroSimuSerializerMetaClass(type(serializers.ModelSerializer)):
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


