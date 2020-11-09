from api.migrations.helper.from_fortran_names_mapper import map_series_to_year_result_creation_kwargs, from_fortran_dict
from api.models.models import LAWMRegionalParameters, LAWMGeneralParameters, LAWMYearResult
from api.std_lib.lawm.regions import DEFAULT_REGIONS


class LAWMAssertsMixin:
    def assert_simu_equivalent_to_std_run(self, simu):
        self.assert_parameters_correspond_to_std_run(simu)
        self.assert_results_correspond_to_std_run(simu)

    def assert_simulations_have_equivalent_region_results(self, first_simu, second_simu):
        first_all_region_results = first_simu.region_results.all()
        second_all_region_results = second_simu.region_results.all()
        self.assert_have_equal_length(first_all_region_results, second_all_region_results)
        for f_reg_res, s_reg_res in zip(first_all_region_results, second_all_region_results):
            self.assert_equal_in_memory_django_models(f_reg_res, s_reg_res)

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

    def assert_parameters_correspond_to_std_run(self, simu):
        run_parameters = simu.run_parameters
        self.assertIsNotNone(run_parameters)
        gen_parameters = run_parameters.general_parameters
        self.assert_general_parameters_were_initialized_correctly(gen_parameters)
        reg_parameters = run_parameters.regional_parameters.all()
        self.assert_regional_parameters_were_initialized_correctly(reg_parameters)

    def assert_results_correspond_to_std_run(self, simu):
        simu_region_results = simu.region_results.all()
        self.assert_has_length(simu_region_results, 4)
        for region_name, df_region in self.STD_RUN_REGIONS_DFS_TUPLES:
            self.assert_region_was_initialized_correctly(simu_region_results, region_name, df_region)

    def assert_region_year_results_correspond_to_csv_values(self, region_year_results, y_series):
        year = y_series["YEAR"]
        db_year_result_qs = region_year_results.filter(year=year)
        self.assert_has_length(db_year_result_qs, 1)
        db_year_result = db_year_result_qs[0]
        csv_year_result_kwargs = map_series_to_year_result_creation_kwargs(y_series)
        csv_year_result = LAWMYearResult(**csv_year_result_kwargs)
        attributes = from_fortran_dict.keys()
        self.assert_equal_values_for_attributes(csv_year_result, db_year_result, attributes)

    def assert_region_was_initialized_correctly(self, simu_region_results, region_name, df_region):
        region_result_qs = simu_region_results.filter(region__name=region_name)
        self.assert_has_length(region_result_qs, 1)
        region_result = region_result_qs[0]
        year_results = region_result.year_results.all()
        years = range(1960, 2001)
        self.assert_have_equal_length(year_results, years)
        for _, y_series in df_region.iterrows():
            self.assert_region_year_results_correspond_to_csv_values(year_results, y_series)
