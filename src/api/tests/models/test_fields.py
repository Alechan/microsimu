from django.core.exceptions import ValidationError
from django.db.models import NOT_PROVIDED
from django.test import TestCase

from api.tests.models.models import *


class VariableFloatFieldTest(TestCase):
    def test_objects_create_with_float_creates_correct_object(self):
        value = 423.32
        model_created = DjangoModelWithVariableFields.objects.create(float_var=value)

        actual_model_variable = model_created.float_var
        expected_model_variable = CustomVariable(value)

        self.assertEqual(actual_model_variable, expected_model_variable)

    def test_objects_create_with_model_variable_creates_correct_object(self):
        expected_model_variable = CustomVariable(423.32)
        model_created = DjangoModelWithVariableFields.objects.create(float_var=expected_model_variable)

        actual_model_variable = model_created.float_var

        self.assertEqual(actual_model_variable, expected_model_variable)


class ParameterBaseFieldTest(TestCase):
    def test_use_parameter_default_is_false_by_default(self):
        expected_default = NOT_PROVIDED
        field = ParameterIntegerField(model_parameter=CustomGeneralParameter)

        actual_default = field.default

        self.assertEqual(expected_default, actual_default)

    def test_use_parameter_default_sets_parameter_default(self):
        expected_default = 5
        field = ParameterIntegerField(model_parameter=CustomGeneralParameter, use_parameter_default=True)

        actual_default = field.default

        self.assertEqual(expected_default, actual_default)

    def test_get_defaults_per_region_throws_exception_with_non_regional_parameter(self):
        field = ParameterIntegerField(model_parameter=CustomGeneralParameter)
        try:
            field.get_defaults_per_region()
            self.fail("The test should've raised an exception but didn't.")
        except TypeError:
            pass

    def test_get_defaults_per_region_returns_correct_object_with_regional_parameter(self):
        expected_defaults_per_region = dict((
            ("developed", 3200),
            ("latinamerica", 3000),
            ("africa", 3000),
            ("asia", 3000)
        ))

        field = ParameterIntegerField(model_parameter=CustomRegionalParameter)
        actual_defaults_per_region = field.get_defaults_per_region()

        self.assertEqual(expected_defaults_per_region, actual_defaults_per_region)

    def test_get_defaults_for_region_returns_correct_object_with_regional_parameter(self):
        expected_default_developed = 3200
        field = ParameterIntegerField(model_parameter=CustomRegionalParameter)
        actual_default_developed = field.get_defaults_for_region("developed")

        self.assertEqual(expected_default_developed, actual_default_developed)

    def test_get_metadata_returns_correct_data(self):
        expected_metadata = {
        "default" : 5,
        "minimum" : 1,
        "maximum" : 10,
        "name" : "The name",
        "fortran_name" : "The fortran name",
        "unit" : "The unit",
        "description" : "The description",
        }
        field = ParameterIntegerField(model_parameter=CustomGeneralParameter)

        actual_metadata = field.get_metadata()

        self.assertEqual(expected_metadata, actual_metadata)


class ParameterIntegerFieldTest(TestCase):
    def test_objects_create_with_integer_creates_correct_object(self):
        value = 423
        model_created = IntegerParameterFieldDjangoModel.objects.create(integer_param=value)

        actual_model_parameter = model_created.integer_param
        expected_model_parameter = CustomGeneralParameter(value)

        self.assertEqual(actual_model_parameter, expected_model_parameter)

    def test_objects_create_with_model_parameter_creates_correct_object(self):
        expected_model_parameter = CustomGeneralParameter(423)
        model_created = IntegerParameterFieldDjangoModel.objects.create(integer_param=expected_model_parameter)

        actual_model_parameter = model_created.integer_param

        self.assertEqual(actual_model_parameter, expected_model_parameter)

    def test_get_from_database_creates_correct_object(self):
        expected_model_parameter = CustomGeneralParameter(423)
        _ = IntegerParameterFieldDjangoModel.objects.create(integer_param=expected_model_parameter)

        model_from_db = IntegerParameterFieldDjangoModel.objects.all()[0]
        actual_model_parameter = model_from_db.integer_param

        self.assertEqual(actual_model_parameter, expected_model_parameter)

    def test_default_value_is_automatically_set_from_parameter_class_object(self):
        expected_value           = CustomGeneralParameter.default
        expected_model_parameter = CustomGeneralParameter(expected_value)

        model_created = IntegerParameterFieldDjangoModel.objects.create()

        actual_model_parameter = model_created.integer_param

        self.assertEqual(actual_model_parameter, expected_model_parameter)

    def test_max_validator_is_automatically_generated(self):
        value = 11
        invalid_model = IntegerParameterFieldDjangoModel(integer_param=value)
        try:
            invalid_model.full_clean()
            self.fail("Creating 2 regions with same name should raise an error.")
        except ValidationError:
            pass

    def test_min_validator_is_automatically_generated(self):
        value = 0
        invalid_model = IntegerParameterFieldDjangoModel(integer_param=value)
        try:
            invalid_model.full_clean()
            self.fail("Creating 2 regions with same name should raise an error.")
        except ValidationError:
            pass


class ParameterFloatFieldTest(TestCase):
    def setUp(self):
        self.value = 423.23

    def test_objects_create_with_integer_creates_correct_object(self):
        model_created = FloatParameterFieldDjangoModel.objects.create(float_param=self.value)

        actual_model_parameter = model_created.float_param
        expected_model_parameter = CustomGeneralParameter(self.value)

        self.assertEqual(actual_model_parameter, expected_model_parameter)

    def test_objects_create_with_model_parameter_creates_correct_object(self):
        expected_model_parameter = CustomGeneralParameter(self.value)
        model_created = FloatParameterFieldDjangoModel.objects.create(float_param=expected_model_parameter)

        actual_model_parameter = model_created.float_param

        self.assertEqual(actual_model_parameter, expected_model_parameter)

    def test_get_from_database_creates_correct_object(self):
        expected_model_parameter = CustomGeneralParameter(self.value)
        _ = FloatParameterFieldDjangoModel.objects.create(float_param=expected_model_parameter)

        model_from_db = FloatParameterFieldDjangoModel.objects.all()[0]
        actual_model_parameter = model_from_db.float_param

        self.assertEqual(actual_model_parameter, expected_model_parameter)

    def test_default_value_is_automatically_set_from_parameter_class_object(self):
        expected_value           = CustomGeneralParameter.default
        expected_model_parameter = CustomGeneralParameter(expected_value)

        model_created = FloatParameterFieldDjangoModel.objects.create()

        actual_model_parameter = model_created.float_param

        self.assertEqual(actual_model_parameter, expected_model_parameter)

