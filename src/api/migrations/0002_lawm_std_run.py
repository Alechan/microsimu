from pathlib import Path

from django.db import migrations, transaction, IntegrityError

import pandas

from api.migrations.csvs.from_fortran_names_mapper import map_series_to_year_result_creation_kwargs

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
    LAWMSimulation   = apps.get_model('api', 'LAWMSimulation')
    LAWMRegion       = apps.get_model('api', 'LAWMRegion')
    LAWMRegionResult = apps.get_model('api', 'LAWMRegionResult')
    LAWMYearResult   = apps.get_model('api', 'LAWMYearResult')

    regions_dfs = [
        ["developed"   , pandas.read_csv(DEVELOPED_CSV_PATH)],
        ["latinamerica", pandas.read_csv(LA_CSV_PATH)],
        ["africa"      , pandas.read_csv(AFRICA_CSV_PATH)],
        ["asia"        , pandas.read_csv(ASIA_CSV_PATH)],
    ]

    try:
        with transaction.atomic():
            objects_to_save = []
            # Instantiations
            simu = create_new_object(LAWMSimulation, {}, objects_to_save)
            for region_name, df_region in regions_dfs:
                region = create_new_object(LAWMRegion, {"name": region_name}, objects_to_save)
                region_result = create_new_object(
                    LAWMRegionResult,
                    {"simulation": simu, "region": region},
                    objects_to_save
                )
                create_year_results(LAWMYearResult, region_result, objects_to_save, df_region)
            # Persistence
            for obj in objects_to_save:
                obj.save()
    except IntegrityError:
        # Rollback
        for obj in objects_to_save:
            obj.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_from_csv),
    ]
