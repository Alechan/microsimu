from unittest import skip
from unittest.mock import Mock, MagicMock

from django import test

from api.serializers.serializer_fields import ParameterIntegerSerializerField
from api.tests.helpers.api_test_mixin import MicroSimuTestMixin
from api.tests.models.models import IntegerParameterFieldDjangoModel, ParameterIntegerField, CustomGeneralParameter


class SerializerFieldsPostgresTest(test.TestCase, MicroSimuTestMixin):
    """
    When using postgres as the DB, django automatically adds "max_value" and "min_value" kwargs
    to the model's field validator, so DRF automatically adds them as kwargs for the serializer
    field. I don't know why they don't add them as proper validators. The server throws a 500
    with the following error (when trying to instantiate a serializer field):
    __init__() got an unexpected keyword argument 'max_value'
    """
    integer_postgres_kwargs = {'required': False, 'max_value': 2147483647, 'min_value': -2147483648, 'validators': []}

    def test_parameter_integer_field_initialization_works_with_postgres(self):
        try:
            ParameterIntegerSerializerField(**self.integer_postgres_kwargs)
        except TypeError:
            error_msg = "The serializer field instantiation raised a TypeError. Are you taking into consideration the " \
                        "automatically added kwargs when using postgres? (max_value, min_value) "
            self.fail(error_msg)

    # noinspection PyPep8Naming
    def test_parameter_integer_field_validation_works_with_postgres(self):
        value = 2000
        FakeSerializer = self.get_fake_serializer(value)

        field = ParameterIntegerSerializerField(**self.integer_postgres_kwargs)
        field.parent = FakeSerializer
        field.source = "a_field"
        try:
            field.run_validation(value)
        except TypeError:
            error_msg = "The serializer field instantiation raised a TypeError. Are you taking into consideration the " \
                        "automatically added kwargs when using postgres? (max_value, min_value) "
            self.fail(error_msg)

    @staticmethod
    def get_fake_serializer(value):
        mock_field_descriptor = Mock()
        mock_field_descriptor.field.to_python = MagicMock(return_value=CustomGeneralParameter(value))

        class FakeModel:
            a_field = mock_field_descriptor

        class FakeSerializer:
            class Meta:
                model = FakeModel

        return FakeSerializer

