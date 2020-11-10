class DjangoAssertsMixin:
    def assert_equal_in_memory_django_models(self, first, second, fields_to_ignore=None):
        """
        Assert that both in-memory objects are equal (no PK or similar taken into consideration)
        """
        first_values = self.get_django_model_dict_values(first)
        second_values = self.get_django_model_dict_values(second)
        if fields_to_ignore:
            first_values = self.remove_fields_from_tuples(fields_to_ignore, first_values)
            second_values = self.remove_fields_from_tuples(fields_to_ignore, second_values)
        self.assertEqual(first_values, second_values)

    @staticmethod
    def remove_fields_from_tuples(fields_to_remove, tuples):
        tuples = [x for x in tuples if x[0] not in fields_to_remove]
        return tuples

    @staticmethod
    def get_django_model_dict_values(obj):
        return [(k, v) for k, v in obj.__dict__.items() if k != '_state']

