import os
from subprocess import DEVNULL
import subprocess
from datetime import datetime

import pandas

from api.settings_api import LAWM_EXECUTABLE_PATH
from api.std_lib.lawm.regions import Developed, Africa, Latinamerica, Asia
from api.std_lib.lawm.simulator.exceptions import ValidInputButSimulationError
from api.std_lib.lawm.simulator.fortran.lawm_fortran_cfg_formatter import LAWMFortranCFGFormatter


class LAWMFortranSimulator:
    sub_folder_name = "tmp"

    def __init__(self, base_path):
        self.dest_path        = base_path / self.sub_folder_name
        self.cfg_formatter    = LAWMFortranCFGFormatter()
        self.cfg_file_name    = "run.cfg"
        self.result_file_name = "result"

    def simulate(self, validated_data):
        cfg_content = self.cfg_formatter.cfg_content_from_validated_data(validated_data)
        timestamp_path = self.mkdir_from_timestamp(self.dest_path)
        cfg_path = timestamp_path / self.cfg_file_name
        self.write_string_to_file(cfg_content, cfg_path)
        command = f"{LAWM_EXECUTABLE_PATH} {self.cfg_file_name} {self.result_file_name}"
        retcode = subprocess.call(command, stdout=DEVNULL, stderr=DEVNULL, shell=True, cwd=timestamp_path)
        if not retcode:
            csv_per_region = {
                Developed.name   : timestamp_path / "result_reg_1_all.csv",
                Latinamerica.name: timestamp_path / "result_reg_2_all.csv",
                Africa.name      : timestamp_path / "result_reg_3_all.csv",
                Asia.name        : timestamp_path / "result_reg_4_all.csv",
            }
            dfs_per_region = {
                reg_name: self.get_df(reg_csv_path) for reg_name, reg_csv_path in csv_per_region.items()
            }
            return dfs_per_region
        else:
            raise ValidInputButSimulationError(f"The FORTRAN LAWM run on path {timestamp_path} returned an error.")

    def write_string_to_file(self, str_, file_path):
        with open(file_path, 'w') as output_file:
            output_file.write(str_)
        return 0

    def mkdir_from_timestamp(self, base_path):
        now = datetime.now()
        new_folder_path = base_path / now.strftime('%Y-%m-%d/%H_%M_%S')
        self.mkdir(new_folder_path)
        return new_folder_path

    def mkdir(self, base_path):
        if not os.path.exists(base_path):
            os.makedirs(base_path)

    @staticmethod
    def get_df(csv_path):
        return pandas.read_csv(csv_path)
