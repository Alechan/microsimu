import pandas

from api.settings_api import LAWM_CSV_PER_REGION
from api.std_lib.lawm.regions import Africa, Latinamerica, Developed, Asia
from api.tests.helpers.database_tree import TestDatabaseTree
from api.tests.helpers.django_asserts_mixin import DjangoAssertsMixin
from api.tests.helpers.general_asserts_mixin import GeneralAssertsMixin
from api.tests.helpers.lawm_asserts_mixin import LAWMAssertsMixin
from microsimu.settings import BASE_DIR


class MicroSimuTestMixin(GeneralAssertsMixin, DjangoAssertsMixin, LAWMAssertsMixin):
    BASE_SERVER_URL     = 'http://testserver'

    STD_RUN_DEVELOPED_CSV_PATH = LAWM_CSV_PER_REGION[Developed.name]
    STD_RUN_LA_CSV_PATH        = LAWM_CSV_PER_REGION[Latinamerica.name]
    STD_RUN_AFRICA_CSV_PATH    = LAWM_CSV_PER_REGION[Africa.name]
    STD_RUN_ASIA_CSV_PATH      = LAWM_CSV_PER_REGION[Asia.name]
    STD_RUN_REGIONS_DFS_TUPLES = [
        [Developed.name, pandas.read_csv(STD_RUN_DEVELOPED_CSV_PATH)],
        [Latinamerica.name, pandas.read_csv(STD_RUN_LA_CSV_PATH)],
        [Africa.name, pandas.read_csv(STD_RUN_AFRICA_CSV_PATH)],
        [Asia.name, pandas.read_csv(STD_RUN_ASIA_CSV_PATH)],
    ]

    @staticmethod
    def create_full_simulation_db_tree():
        return TestDatabaseTree()

    @staticmethod
    def get_year_result_creation_kwargs(region_result, year):
        return TestDatabaseTree.get_year_result_creation_kwargs(region_result, year)
