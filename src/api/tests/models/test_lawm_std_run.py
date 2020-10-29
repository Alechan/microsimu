import pandas
from django.test import TestCase

from api.migrations.csvs.from_fortran_names_mapper import map_series_to_year_result_creation_kwargs, from_fortran_dict
from api.models.models import LAWMSimulation, LAWMYearResult
from api.tests.api_test_mixin import ApiTestMixin


class LAWMRegionTest(TestCase, ApiTestMixin):

    @classmethod
    def setUpTestData(cls):
        developed_csv_path = cls.get_migrations_csvs_path() / "fortran_std_developed.csv"
        la_csv_path        = cls.get_migrations_csvs_path() / "fortran_std_la.csv"
        africa_csv_path    = cls.get_migrations_csvs_path() / "fortran_std_africa.csv"
        asia_csv_path      = cls.get_migrations_csvs_path() / "fortran_std_asia.csv"
        cls.regions_dfs = [
            ["developed"   , pandas.read_csv(developed_csv_path)],
            ["latinamerica", pandas.read_csv(la_csv_path)],
            ["africa"      , pandas.read_csv(africa_csv_path)],
            ["asia"        , pandas.read_csv(asia_csv_path)],
        ]

    def test_first_simulation_corresponds_to_std_run(self):
        simus = LAWMSimulation.objects.filter(pk=1)

        self.assert_has_length(simus, 1)
        simu = simus[0]
        simu_region_results = simu.region_results.all()
        self.assert_has_length(simu_region_results, 4)

        for region_name, df_region in self.regions_dfs:
            self.assert_region_was_initialized_correctly(simu_region_results, region_name, df_region)

    def assert_region_was_initialized_correctly(self, simu_region_results, region_name, df_region):
        developed_region_result_qs = simu_region_results.filter(region__name=region_name)
        self.assert_has_length(developed_region_result_qs, 1)
        developed_region_result = developed_region_result_qs[0]
        developed_year_results = developed_region_result.year_results.all()
        years = range(1960, 2001)
        self.assert_have_equal_length(developed_year_results, years)
        for _, y_series in df_region.iterrows():
            self.assert_region_year_results_correspond_to_csv_values(developed_year_results, y_series)

    def assert_region_year_results_correspond_to_csv_values(self, region_year_results, y_series):
        year = y_series["YEAR"]
        db_year_result_qs = region_year_results.filter(year=year)
        self.assert_has_length(db_year_result_qs, 1)
        db_year_result = db_year_result_qs[0]
        csv_year_result_kwargs = map_series_to_year_result_creation_kwargs(y_series)
        csv_year_result = LAWMYearResult(**csv_year_result_kwargs)
        attributes = from_fortran_dict.keys()
        self.assert_equal_values_for_attributes(csv_year_result, db_year_result, attributes)
