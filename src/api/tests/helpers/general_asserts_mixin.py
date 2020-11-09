import filecmp
from datetime import datetime, timedelta


class GeneralAssertsMixin:
    def assert_not_empty(self, collection):
        not_empty = len(collection) > 0
        if not not_empty:
            self.fail("The collection is empty.")

    def assert_is_later_and_close(self, after_time_iso, before_time_iso):
        self.assertGreater(after_time_iso, before_time_iso)
        actual_time = datetime.fromisoformat(after_time_iso)
        expected_time = datetime.fromisoformat(before_time_iso)
        actual_timedelta = abs(actual_time - expected_time)
        max_timedelta = timedelta(seconds=10)
        if actual_timedelta > max_timedelta:
            self.fail(f"The expected time {expected_time} is not close to the actual time {actual_time}.")

    def assert_have_equal_length(self, first, second):
        if len(first) != len(second):
            self.fail(f"The first had length {len(first)} but the second had length {len(second)}")

    def assert_has_length(self, collection, length):
        if len(collection) != length:
            self.fail(f"The collection had length {len(collection)} but it was expected to be {length}")

    def assert_equal_values_for_attributes(self, first, second, attributes):
        for attr in attributes:
            self.assertEqual(getattr(first, attr), getattr(second, attr))

    def assert_dicts_equal(self, first, second, **kwargs):
        # If they are not dicts, use the default assertEqual
        self.assert_both_are_dicts(first, second)

        # They are both dicts, use step by step comparison
        # noinspection PyTypeChecker
        self.assertEqual(first.keys(), second.keys())
        for key in first:
            first_value = first[key]
            second_value = second[key]
            # self.assertEqual(first_value, second_value, **kwargs)
            try:
                self.assert_both_are_dicts(first_value, second_value)
                self.assert_dicts_equal(first_value, second_value)
            except AssertionError:
                self.assertEqual(first_value, second_value, **kwargs)

    def assert_both_are_dicts(self, first, second):
        first_is_dict = isinstance(first, dict)
        second_is_dict = isinstance(second, dict)
        if not (first_is_dict and second_is_dict):
            if not first_is_dict:
                self.fail("The first argument wasn't a dict.")
            else:
                self.fail("The second argument wasn't a dict.")

    def assert_files_equal(self, first, second):
        comparison = filecmp.cmp(first, second)
        if not comparison:
            self.fail(f"The files {first} and {second} are not equal")

    def assert_dfs_equal(self, first, second):
        bool_mask = first == second
        all_true = bool_mask.all(axis=None)
        if not all_true:
            self.fail("The dfs are not equal")
