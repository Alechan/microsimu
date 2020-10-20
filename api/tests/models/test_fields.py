from django.test import TestCase

from api.tests.models.models import DjangoModelWithCustomFields, CustomVariable


class VariableFloatFieldTest(TestCase):
    def test_objects_create_with_float_creates_correct_object(self):
        value = 423.32
        model_created = DjangoModelWithCustomFields.objects.create(float_var=value)

        self.assertEqual(model_created.float_var, CustomVariable(value))

    def test_objects_create_with_model_variable_creates_correct_object(self):
        value = CustomVariable(423.32)
        model_created = DjangoModelWithCustomFields.objects.create(float_var=value)

        self.assertEqual(model_created.float_var, value)

