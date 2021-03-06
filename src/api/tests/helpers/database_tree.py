from api.models.models import LAWMSimulation, LAWMRegion, LAWMRegionResult, LAWMGeneralParameters, LAWMRunParameters, \
    LAWMRegionalParameters, LAWMYearResult
from api.std_lib.lawm.regions import Africa, Asia, Developed, Latinamerica


class TestDatabaseTree:
    def __init__(self):
        self.simu    = LAWMSimulation.objects.create()
        self.region_africa = LAWMRegion.objects.get_or_create(name=Africa.name)[0]
        self.region_asia = LAWMRegion.objects.get_or_create(name=Asia.name)[0]
        self.region_developed = LAWMRegion.objects.get_or_create(name=Developed.name)[0]
        self.region_la = LAWMRegion.objects.get_or_create(name=Latinamerica.name)[0]
        self.region_result_r1 = LAWMRegionResult.objects.create(simulation=self.simu, region=self.region_africa)
        self.region_result_r2 = LAWMRegionResult.objects.create(simulation=self.simu, region=self.region_developed)
        self.year_results_reg_1 = self.create_year_results(self.region_result_r1, n_years=2)
        self.year_results_reg_2 = self.create_year_results(self.region_result_r2, n_years=2)
        self.general_parameters  = LAWMGeneralParameters.objects.create(simulation_stop=2001)
        self.run_parameters      = LAWMRunParameters.objects.create(
            general_parameters=self.general_parameters,
            simulation=self.simu
        )
        self.regional_parameters_developed = LAWMRegionalParameters.new_with_defaults_for_region(self.run_parameters, self.region_developed)
        self.regional_parameters_latinamerica = LAWMRegionalParameters.new_with_defaults_for_region(self.run_parameters, self.region_la)
        self.regional_parameters_africa = LAWMRegionalParameters.new_with_defaults_for_region(self.run_parameters, self.region_africa)
        self.regional_parameters_asia = LAWMRegionalParameters.new_with_defaults_for_region(self.run_parameters, self.region_asia)
        self.all_reg_params = [
            self.regional_parameters_developed,
            self.regional_parameters_latinamerica,
            self.regional_parameters_africa,
            self.regional_parameters_asia,
        ]

    @classmethod
    def create_year_results(cls, region_result, n_years):
        year_results = []
        for i_y in range(n_years):
            year = 1960 + i_y
            creation_kwargs = cls.get_year_result_creation_kwargs(region_result, year=year)
            y_res = LAWMYearResult.objects.create(**creation_kwargs)
            year_results.append(y_res)
        return year_results

    @staticmethod
    def get_year_result_creation_kwargs(region_result, year=1960):
        return {
            "region_result": region_result,
            "year"      : year,
            "pop"       : 123,
            "popr"      : 124,
            "exlife"    : 125,
            "grmor"     : 126,
            "birthr"    : 127,
            "chmor"     : 128,
            "calor"     : 129,
            "prot"      : 130,
            "hsexfl"    : 131,
            "gnpxc"     : 132,
            "enrol"     : 133,
            "educr"     : 134,
            "eapopr"    : 135,
            "tlf"       : 136,
            "rlfd_1"    : 137,
            "rlfd_2"    : 138,
            "rlfd_3"    : 139,
            "rlfd_4"    : 140,
            "rlfd_5"    : 141,
            "capt"      : 142,
            "capd_1"    : 143,
            "capd_2"    : 144,
            "capd_3"    : 145,
            "capd_4"    : 146,
            "capd_5"    : 147,
            "_0_5"      : 148,
            "_6_17"     : 149,
            "_11_70"    : 150,
            "al"        : 151,
            "excal"     : 152,
            "fert"      : 153,
            "rend"      : 154,
            "falu"      : 155,
            "urbanr"    : 156,
            "turbh"     : 157,
            "sepopr"    : 158,
            "houser"    : 159,
            "perxfl"    : 160,
            "gnp"       : 161,
            "gnpd_1"    : 162,
            "gnpd_2"    : 163,
            "gnpd_3"    : 164,
            "gnpd_4"    : 165,
            "gnpd_5"    : 166,

        }