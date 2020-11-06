from datetime import datetime, timedelta

from api.models.models import *
from microsimu.settings import BASE_DIR


class TestDatabaseTree:
    def __init__(self):
        self.simu    = LAWMSimulation.objects.create()
        self.region_1 = LAWMRegion.objects.get_or_create(name="africa")[0]
        self.region_2 = LAWMRegion.objects.get_or_create(name="developed")[0]
        self.region_result_r1 = LAWMRegionResult.objects.create(simulation=self.simu, region=self.region_1)
        self.region_result_r2 = LAWMRegionResult.objects.create(simulation=self.simu, region=self.region_2)
        self.year_results_reg_1 = self.create_year_results(self.region_result_r1, n_years=2)
        self.year_results_reg_2 = self.create_year_results(self.region_result_r2, n_years=2)
        self.general_parameters  = GeneralParameters.objects.create(simulation_stop=2001)
        self.run_parameters      = LAWMRunParameters.objects.create(
            general_parameters=self.general_parameters,
            simulation=self.simu
        )
        self.regional_parameters_developed = RegionalParameters.new_with_defaults_for_region(self.run_parameters, self.region_1)

    @classmethod
    def create_year_results(cls, region_result, n_years):
        year_results = []
        for i_y in range(n_years):
            year = 1960 + i_y
            creation_kwargs = cls.get_year_result_creation_kwargs(region_result, year=year)
            y_res = LAWMYearResult.objects.create(**creation_kwargs)
            year_results.append(y_res)
        return year_results

    @staticmethod
    def get_year_result_creation_kwargs(region_result, year=1960):
        return {
            "region_result": region_result,
            "year"      : year,
            "pop"       : 123,
            "popr"      : 124,
            "exlife"    : 125,
            "grmor"     : 126,
            "birthr"    : 127,
            "chmor"     : 128,
            "calor"     : 129,
            "prot"      : 130,
            "hsexfl"    : 131,
            "gnpxc"     : 132,
            "enrol"     : 133,
            "educr"     : 134,
            "eapopr"    : 135,
            "tlf"       : 136,
            "rlfd_1"    : 137,
            "rlfd_2"    : 138,
            "rlfd_3"    : 139,
            "rlfd_4"    : 140,
            "rlfd_5"    : 141,
            "capt"      : 142,
            "capd_1"    : 143,
            "capd_2"    : 144,
            "capd_3"    : 145,
            "capd_4"    : 146,
            "capd_5"    : 147,
            "_0_5"      : 148,
            "_6_17"     : 149,
            "_11_70"    : 150,
            "al"        : 151,
            "excal"     : 152,
            "fert"      : 153,
            "rend"      : 154,
            "falu"      : 155,
            "urbanr"    : 156,
            "turbh"     : 157,
            "sepopr"    : 158,
            "houser"    : 159,
            "perxfl"    : 160,
            "gnp"       : 161,
            "gnpd_1"    : 162,
            "gnpd_2"    : 163,
            "gnpd_3"    : 164,
            "gnpd_4"    : 165,
            "gnpd_5"    : 166,

        }


class ApiTestMixin:
    BASE_SERVER_URL     = 'http://testserver'
    MIGRATIONS_CSV_PATH = BASE_DIR / "api" / "migrations" / "csvs"

    @staticmethod
    def create_full_simulation_db_tree():
        return TestDatabaseTree()

    @staticmethod
    def get_year_result_creation_kwargs(region_result, year):
        return TestDatabaseTree.get_year_result_creation_kwargs(region_result, year)

    def assert_is_later_and_close(self, after_time_iso, before_time_iso):
        self.assertGreater(after_time_iso, before_time_iso)
        actual_time   = datetime.fromisoformat(after_time_iso)
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
        if not (isinstance(first, dict) and isinstance(second, dict)):
            self.fail("One of the arguments wasn't a dict.")

        # They are both dicts, use step by step comparison
        # noinspection PyTypeChecker
        self.assertEqual(first.keys(), second.keys())
        for key in first:
            self.assertEqual(first[key], second[key], **kwargs)

