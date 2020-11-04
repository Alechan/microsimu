from django.test import TestCase

from api.tests.models.models import DjangoModelWithVariableFields, CustomVariable, DjangoModelWithParameterFields, \
    CustomParameter


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


class ParameterFloatFieldTest(TestCase):
    def test_objects_create_with_float_creates_correct_object(self):
        value = 423
        model_created = DjangoModelWithParameterFields.objects.create(integer_param=value)

        actual_model_variable = model_created.integer_param
        expected_model_variable = CustomParameter(value)

        self.assertEqual(actual_model_variable, expected_model_variable)

    def test_objects_create_with_model_variable_creates_correct_object(self):
        self.fail("Adaptar a parameter")
        expected_model_variable = CustomVariable(423.32)
        model_created = DjangoModelWithVariableFields.objects.create(float_var=expected_model_variable)

        actual_model_variable = model_created.float_var

        self.assertEqual(actual_model_variable, expected_model_variable)
