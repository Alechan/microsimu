from django.db import transaction, IntegrityError
from api.migrations.helper.from_fortran_names_mapper import map_series_to_year_result_creation_kwargs
from api.models.models import LAWMRegionalParameters as VOLATILE_LAWMRegionalParameters


def load_lawm_run_to_db(dfs_per_region):
    """
    Loads the pandas dataframes into the database. The django models imports are inside the
    function to avoid ambiguity with the "migration imports" done for the raw version
    of the function in the migrations file.

    :param dfs_per_region: a dict of {region.name : df_region}
    :return:
    """

    from api.models.models import LAWMGeneralParameters, \
        LAWMRunParameters, LAWMSimulation, LAWMRegion, LAWMYearResult, LAWMRegionResult, LAWMRegionalParameters

    return load_lawm_run_to_db_raw(LAWMGeneralParameters, LAWMRegion, LAWMRegionResult, LAWMRegionalParameters,
                                   LAWMRunParameters, LAWMSimulation, LAWMYearResult, dfs_per_region,
                                   create_regions=False,
                                   create_parameters=False)


def load_lawm_run_to_db_raw(LAWMGeneralParameters, LAWMRegion, LAWMRegionResult, LAWMRegionalParameters,
                            LAWMRunParameters, LAWMSimulation, LAWMYearResult, regions_dfs,
                            create_regions=True, create_parameters=True):
    try:
        with transaction.atomic():
            objects_to_save = []
            # Instantiations
            simu = create_new_object(LAWMSimulation, {}, objects_to_save)
            if create_parameters:
                gen_params = create_new_object(LAWMGeneralParameters, {}, objects_to_save)
                run_parameters = create_new_object(
                    LAWMRunParameters,
                    {"simulation": simu, "general_parameters": gen_params},
                    objects_to_save
                )
            for region_name, df_region in regions_dfs.items():
                if create_regions:
                    region = create_new_object(LAWMRegion, {"name": region_name}, objects_to_save)
                else:
                    region = LAWMRegion.objects.get(name=region_name)
                create_region_result(LAWMRegionResult, LAWMYearResult, df_region, objects_to_save, region, simu)
                if create_parameters:
                    create_region_parameters(LAWMRegionalParameters, objects_to_save, region, region_name, run_parameters)
            # Persistence
            for obj in objects_to_save:
                obj.save()
            return simu
    except IntegrityError:
        # Rollback
        for obj in objects_to_save:
            obj.delete()


def create_new_object(cls, kwargs, objects_to_save):
    obj = cls(**kwargs)
    objects_to_save.append(obj)
    return obj


def create_year_results(LAWMYearResult, region_result, objects_to_save, df_region):
    for _, y_series in df_region.iterrows():
        year_result_creation_kwargs = map_series_to_year_result_creation_kwargs(y_series)
        year_result_creation_kwargs["region_result"] = region_result
        year_result = create_new_object(LAWMYearResult, year_result_creation_kwargs, objects_to_save)


def create_region_parameters(LAWMRegionalParameters, objects_to_save, region, region_name, run_parameters):
    # CAREFUL!
    # We are using the models.py class to use its classmethod, but only because this
    # method has no side effect and doesn't modify the database
    partial_kwargs = VOLATILE_LAWMRegionalParameters.get_default_values_for_region(region_name)
    reg_params_kwargs = partial_kwargs | {"run_parameters": run_parameters, "region": region}
    reg_params = create_new_object(LAWMRegionalParameters, reg_params_kwargs, objects_to_save)


def create_region_result(LAWMRegionResult, LAWMYearResult, df_region, objects_to_save, region, simu):
    region_result = create_new_object(
        LAWMRegionResult,
        {"simulation": simu, "region": region},
        objects_to_save
    )
    create_year_results(LAWMYearResult, region_result, objects_to_save, df_region)