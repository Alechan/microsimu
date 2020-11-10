from pathlib import Path

from api.std_lib.lawm.regions import *

THIS_FILE_PATH           = Path(__file__).resolve()

API_APP_PATH             = THIS_FILE_PATH.parent

LAWM_PATH                = API_APP_PATH / "std_lib" / "lawm"
LAWM_RUNS_FOLDER_PATH    = LAWM_PATH / "runs"
LAWM_STD_RUN_FOLDER_PATH = LAWM_RUNS_FOLDER_PATH / "std_run"
LAWM_CSV_PER_REGION = {
    Developed.name    : LAWM_STD_RUN_FOLDER_PATH / "fortran_std_developed.csv",
    Latinamerica.name : LAWM_STD_RUN_FOLDER_PATH / "fortran_std_la.csv",
    Africa.name       : LAWM_STD_RUN_FOLDER_PATH / "fortran_std_africa.csv",
    Asia.name         : LAWM_STD_RUN_FOLDER_PATH / "fortran_std_asia.csv",
}
