from pathlib import Path

from django.db import migrations, transaction, IntegrityError

import pandas

from api.migrations.csvs.from_fortran_names_mapper import map_series_to_year_result_creation_kwargs
from api.models.models import LAWMRegionalParameters as VOLATILE_LAWMRegionalParameters

MIGRATIONS_PATH = Path(__file__).resolve().parent
CSVS_PATH = MIGRATIONS_PATH / "csvs"

DEVELOPED_CSV_PATH = CSVS_PATH / "fortran_std_developed.csv"
LA_CSV_PATH        = CSVS_PATH / "fortran_std_la.csv"
AFRICA_CSV_PATH    = CSVS_PATH / "fortran_std_africa.csv"
ASIA_CSV_PATH      = CSVS_PATH / "fortran_std_asia.csv"


def create_new_object(cls, kwargs, objects_to_save):
    obj = cls(**kwargs)
    objects_to_save.append(obj)
    return obj


# noinspection PyPep8Naming
def create_year_results(LAWMYearResult, region_result, objects_to_save, df_region):
    for _, y_series in df_region.iterrows():
        year_result_creation_kwargs = map_series_to_year_result_creation_kwargs(y_series)
        year_result_creation_kwargs["region_result"] = region_result
        year_result = create_new_object(LAWMYearResult, year_result_creation_kwargs, objects_to_save)


# noinspection PyPep8Naming
def load_from_csv(apps, schema_editor):
    LAWMSimulation         = apps.get_model('api', 'LAWMSimulation')
    LAWMRegion             = apps.get_model('api', 'LAWMRegion')
    LAWMRegionResult       = apps.get_model('api', 'LAWMRegionResult')
    LAWMYearResult         = apps.get_model('api', 'LAWMYearResult')
    LAWMRunParameters      = apps.get_model('api', 'LAWMRunParameters')
    LAWMGeneralParameters  = apps.get_model('api', 'LAWMGeneralParameters')
    LAWMRegionalParameters = apps.get_model('api', 'LAWMRegionalParameters')

    regions_dfs = [
        ["developed"   , pandas.read_csv(DEVELOPED_CSV_PATH)],
        ["latinamerica", pandas.read_csv(LA_CSV_PATH)],
        ["africa"      , pandas.read_csv(AFRICA_CSV_PATH)],
        ["asia"        , pandas.read_csv(ASIA_CSV_PATH)],
    ]

    all_region_names = [x[0] for x in regions_dfs]

    try:
        with transaction.atomic():
            objects_to_save = []
            # Instantiations
            simu = create_new_object(LAWMSimulation, {}, objects_to_save)
            gen_params = create_new_object(LAWMGeneralParameters, {}, objects_to_save)
            run_parameters = create_new_object(
                LAWMRunParameters,
                {"simulation": simu, "general_parameters": gen_params},
                objects_to_save
            )
            for region_name, df_region in regions_dfs:
                region = create_new_object(LAWMRegion, {"name": region_name}, objects_to_save)
                create_region_result(LAWMRegionResult, LAWMYearResult, df_region, objects_to_save, region, simu)
                create_region_parameters(LAWMRegionalParameters, objects_to_save, region, region_name, run_parameters)
            # Persistence
            for obj in objects_to_save:
                obj.save()
    except IntegrityError:
        # Rollback
        for obj in objects_to_save:
            obj.delete()


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


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_from_csv),
    ]
