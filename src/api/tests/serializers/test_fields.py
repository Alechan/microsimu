from django import test

from api.serializers.serializer_fields import ParameterIntegerSerializerField
from api.tests.api_test_mixin import MicroSimuTestMixin


class SerializerFieldsPostgresTest(test.TestCase, MicroSimuTestMixin):
    """
    When using postgres as the DB, django automatically adds "max_value" and "min_value" kwargs
    to the model's field validator, so DRF automatically adds them as kwargs for the serializer
    field. I don't know why they don't add them as proper validators. The server throws a 500
    with the following error (when trying to instantiate a serializer field):
    __init__() got an unexpected keyword argument 'max_value'
    """
    integer_postgres_kwargs = {'required': False, 'max_value': 2147483647, 'min_value': -2147483648, 'validators': []}

    def test_parameter_integer_field_works_with_postgres(self):
        try:
            ParameterIntegerSerializerField(**self.integer_postgres_kwargs)
        except TypeError:
            error_msg = "The serializer field instantiation raised a TypeError. Are you taking into consideration the " \
                        "automatically added kwargs when using postgres? (max_value, min_value) "
            self.fail(error_msg)

