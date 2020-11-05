import django
from django.core.exceptions import ValidationError
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


class ParameterIntegerFieldTest(TestCase):
    def test_objects_create_with_integer_creates_correct_object(self):
        value = 423
        model_created = IntegerParameterFieldDjangoModel.objects.create(integer_param=value)

        actual_model_parameter = model_created.integer_param
        expected_model_parameter = CustomParameter(value)

        self.assertEqual(actual_model_parameter, expected_model_parameter)

    def test_objects_create_with_model_parameter_creates_correct_object(self):
        expected_model_parameter = CustomParameter(423)
        model_created = IntegerParameterFieldDjangoModel.objects.create(integer_param=expected_model_parameter)

        actual_model_parameter = model_created.integer_param

        self.assertEqual(actual_model_parameter, expected_model_parameter)

    def test_get_from_database_creates_correct_object(self):
        expected_model_parameter = CustomParameter(423)
        _ = IntegerParameterFieldDjangoModel.objects.create(integer_param=expected_model_parameter)

        model_from_db = IntegerParameterFieldDjangoModel.objects.all()[0]
        actual_model_parameter = model_from_db.integer_param

        self.assertEqual(actual_model_parameter, expected_model_parameter)

    def test_default_value_is_automatically_set_from_parameter_class_object(self):
        expected_value           = CustomParameter.default
        expected_model_parameter = CustomParameter(expected_value)

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
        expected_model_parameter = CustomParameter(self.value)

        self.assertEqual(actual_model_parameter, expected_model_parameter)

    def test_objects_create_with_model_parameter_creates_correct_object(self):
        expected_model_parameter = CustomParameter(self.value)
        model_created = FloatParameterFieldDjangoModel.objects.create(float_param=expected_model_parameter)

        actual_model_parameter = model_created.float_param

        self.assertEqual(actual_model_parameter, expected_model_parameter)

    def test_get_from_database_creates_correct_object(self):
        expected_model_parameter = CustomParameter(self.value)
        _ = FloatParameterFieldDjangoModel.objects.create(float_param=expected_model_parameter)

        model_from_db = FloatParameterFieldDjangoModel.objects.all()[0]
        actual_model_parameter = model_from_db.float_param

        self.assertEqual(actual_model_parameter, expected_model_parameter)

    def test_default_value_is_automatically_set_from_parameter_class_object(self):
        expected_value           = CustomParameter.default
        expected_model_parameter = CustomParameter(expected_value)

        model_created = FloatParameterFieldDjangoModel.objects.create()

        actual_model_parameter = model_created.float_param

        self.assertEqual(actual_model_parameter, expected_model_parameter)

