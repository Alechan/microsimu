import pandas
from django.test import TestCase

from api.migrations.csvs.from_fortran_names_mapper import map_series_to_year_result_creation_kwargs, from_fortran_dict
from api.models.models import LAWMSimulation, LAWMYearResult, LAWMGeneralParameters, LAWMRegionalParameters
from api.std_lib.lawm.regions import Developed, Latinamerica, Africa, Asia, DEFAULT_REGIONS
from api.tests.api_test_mixin import MicroSimuTestMixin


class LAWMRegionTest(TestCase, MicroSimuTestMixin):

    @classmethod
    def setUpTestData(cls):
        developed_csv_path = cls.MIGRATIONS_CSV_PATH / "fortran_std_developed.csv"
        la_csv_path        = cls.MIGRATIONS_CSV_PATH / "fortran_std_la.csv"
        africa_csv_path    = cls.MIGRATIONS_CSV_PATH / "fortran_std_africa.csv"
        asia_csv_path      = cls.MIGRATIONS_CSV_PATH / "fortran_std_asia.csv"
        cls.regions_dfs = [
            [Developed.name   , pandas.read_csv(developed_csv_path)],
            [Latinamerica.name, pandas.read_csv(la_csv_path)],
            [Africa.name      , pandas.read_csv(africa_csv_path)],
            [Asia.name        , pandas.read_csv(asia_csv_path)],
        ]

    def test_first_simulation_corresponds_to_std_run(self):
        simus = LAWMSimulation.objects.filter(pk=1)

        self.assert_has_length(simus, 1)
        simu = simus[0]

        self.assert_parameters_were_initialized_correctly(simu)

        self.assert_results_were_initialized_correctly(simu)

    def assert_parameters_were_initialized_correctly(self, simu):
        run_parameters = simu.run_parameters
        self.assertIsNotNone(run_parameters)
        gen_parameters = run_parameters.general_parameters
        self.assert_general_parameters_were_initialized_correctly(gen_parameters)
        reg_parameters = run_parameters.regional_parameters.all()
        self.assert_regional_parameters_were_initialized_correctly(reg_parameters)

    def assert_regional_parameters_were_initialized_correctly(self, reg_parameters):
        self.assertIsNotNone(reg_parameters)
        reg_params_per_region = LAWMRegionalParameters.new_in_memory_with_defaults_all_regions()
        for reg in DEFAULT_REGIONS:
            region_name = reg.name
            potential_regions = reg_parameters.filter(region__name=region_name)
            self.assert_has_length(potential_regions, 1)
            db_region_params = potential_regions[0]
            expected_region_params = reg_params_per_region[region_name]
            fields_to_ignore = ["id", "run_parameters_id"]
            self.assert_equal_in_memory_django_models(expected_region_params, db_region_params, fields_to_ignore)

    def assert_general_parameters_were_initialized_correctly(self, gen_parameters):
        self.assertIsNotNone(gen_parameters)
        expected_gen_parameters = LAWMGeneralParameters()

        fields_to_ignore = ["id"]
        self.assert_equal_in_memory_django_models(gen_parameters, expected_gen_parameters, fields_to_ignore)

    def assert_results_were_initialized_correctly(self, simu):
        simu_region_results = simu.region_results.all()
        self.assert_has_length(simu_region_results, 4)
        for region_name, df_region in self.regions_dfs:
            self.assert_region_was_initialized_correctly(simu_region_results, region_name, df_region)

    def assert_region_was_initialized_correctly(self, simu_region_results, region_name, df_region):
        region_result_qs = simu_region_results.filter(region__name=region_name)
        self.assert_has_length(region_result_qs, 1)
        region_result = region_result_qs[0]
        year_results = region_result.year_results.all()
        years = range(1960, 2001)
        self.assert_have_equal_length(year_results, years)
        for _, y_series in df_region.iterrows():
            self.assert_region_year_results_correspond_to_csv_values(year_results, y_series)

    def assert_region_year_results_correspond_to_csv_values(self, region_year_results, y_series):
        year = y_series["YEAR"]
        db_year_result_qs = region_year_results.filter(year=year)
        self.assert_has_length(db_year_result_qs, 1)
        db_year_result = db_year_result_qs[0]
        csv_year_result_kwargs = map_series_to_year_result_creation_kwargs(y_series)
        csv_year_result = LAWMYearResult(**csv_year_result_kwargs)
        attributes = from_fortran_dict.keys()
        self.assert_equal_values_for_attributes(csv_year_result, db_year_result, attributes)
