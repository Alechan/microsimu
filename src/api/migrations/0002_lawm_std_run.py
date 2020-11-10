import pandas
from django.db import migrations

from api.migrations.helper.db_models_from_dfs import load_lawm_run_to_db_raw
from api.settings_api import LAWM_CSV_PER_REGION
from api.std_lib.lawm.regions import *

DEVELOPED_CSV_PATH = LAWM_CSV_PER_REGION[Developed.name]
LA_CSV_PATH        = LAWM_CSV_PER_REGION[Latinamerica.name]
AFRICA_CSV_PATH    = LAWM_CSV_PER_REGION[Africa.name]
ASIA_CSV_PATH      = LAWM_CSV_PER_REGION[Asia.name]


# noinspection PyPep8Naming
def load_std_run(apps, schema_editor):
    LAWMSimulation         = apps.get_model('api', 'LAWMSimulation')
    LAWMRegion             = apps.get_model('api', 'LAWMRegion')
    LAWMRegionResult       = apps.get_model('api', 'LAWMRegionResult')
    LAWMYearResult         = apps.get_model('api', 'LAWMYearResult')
    LAWMRunParameters      = apps.get_model('api', 'LAWMRunParameters')
    LAWMGeneralParameters  = apps.get_model('api', 'LAWMGeneralParameters')
    LAWMRegionalParameters = apps.get_model('api', 'LAWMRegionalParameters')

    regions_dfs = {
        "developed"   : pandas.read_csv(DEVELOPED_CSV_PATH),
        "latinamerica": pandas.read_csv(LA_CSV_PATH),
        "africa"      : pandas.read_csv(AFRICA_CSV_PATH),
        "asia"        : pandas.read_csv(ASIA_CSV_PATH),
    }

    load_lawm_run_to_db_raw(LAWMGeneralParameters, LAWMRegion, LAWMRegionResult, LAWMRegionalParameters,
                            LAWMRunParameters, LAWMSimulation, LAWMYearResult, regions_dfs)


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_std_run),
    ]
