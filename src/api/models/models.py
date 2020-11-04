from django.db import models

from api.models.fields import VariableFloatFieldMixin
from api.std_lib.lawm.variables import *


class LAWMRegion(models.Model):
    name = models.CharField(max_length=100, primary_key=True)


class LAWMSimulation(models.Model):
    created = models.DateTimeField(auto_now_add=True)


class LAWMRegionResult(models.Model):
    simulation = models.ForeignKey(LAWMSimulation, related_name="region_results", null=False, on_delete=models.CASCADE)
    region     = models.ForeignKey(LAWMRegion    , related_name="region_result", null=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('simulation', 'region')

    @property
    def region_name(self):
        return self.region.name

    def get_variables_information(self):
        if hasattr(self.__class__, "_cached_vars_info"):
            return self.__class__._cached_vars_info
        else:
            any_result = self.year_results.first()
            vars_info = any_result.get_variables_information()
            self.__class__._cached_vars_info = vars_info
            return vars_info


class LAWMYearResult(models.Model):
    region_result = models.ForeignKey(LAWMRegionResult, related_name="year_results", null=False, on_delete=models.CASCADE)
    year          = models.IntegerField(null=False)
    pop           = VariableFloatFieldMixin(model_variable=Population, null=False)
    popr          = VariableFloatFieldMixin(model_variable=PopulationGrowth, null=False)
    exlife        = VariableFloatFieldMixin(model_variable=LifeExpectancy, null=False)
    grmor         = VariableFloatFieldMixin(model_variable=GrossMortality, null=False)
    birthr        = VariableFloatFieldMixin(model_variable=BirthRate, null=False)
    chmor         = VariableFloatFieldMixin(model_variable=ChildMortalityRate, null=False)
    calor         = VariableFloatFieldMixin(model_variable=Calories, null=False)
    prot          = VariableFloatFieldMixin(model_variable=Proteins, null=False)
    hsexfl        = VariableFloatFieldMixin(model_variable=HousesPerFamily, null=False)
    gnpxc         = VariableFloatFieldMixin(model_variable=GNPPerPerson, null=False)
    enrol         = VariableFloatFieldMixin(model_variable=EnrolmentPercentage, null=False)
    educr         = VariableFloatFieldMixin(model_variable=MatriculationPercentage, null=False)
    eapopr        = VariableFloatFieldMixin(model_variable=Pop11To70LaborForcePercentage, null=False)
    tlf           = VariableFloatFieldMixin(model_variable=TotalLaborForce, null=False)
    rlfd_1        = VariableFloatFieldMixin(model_variable=LaborForceFoodSectorProportion, null=False)
    rlfd_2        = VariableFloatFieldMixin(model_variable=LaborForceHousingSectorProportion, null=False)
    rlfd_3        = VariableFloatFieldMixin(model_variable=LaborForceEducationSectorProportion, null=False)
    rlfd_4        = VariableFloatFieldMixin(model_variable=LaborForceOtherGoodsProportion, null=False)
    rlfd_5        = VariableFloatFieldMixin(model_variable=LaborForceCapitalGoodsSectorProportion, null=False)
    capt          = VariableFloatFieldMixin(model_variable=TotalCapital, null=False)
    capd_1        = VariableFloatFieldMixin(model_variable=CapitalFoodSectorProportion, null=False)
    capd_2        = VariableFloatFieldMixin(model_variable=CapitalHousingSectorProportion, null=False)
    capd_3        = VariableFloatFieldMixin(model_variable=CapitalEducationSectorProportion, null=False)
    capd_4        = VariableFloatFieldMixin(model_variable=CapitalOtherGoodsSectorProportion, null=False)
    capd_5        = VariableFloatFieldMixin(model_variable=CapitalCapitalGoodsSectorProportion, null=False)
    _0_5          = VariableFloatFieldMixin(model_variable=Pop0to5Percentage, null=False)
    _6_17         = VariableFloatFieldMixin(model_variable=Pop6to17Percentage, null=False)
    _11_70        = VariableFloatFieldMixin(model_variable=Pop11to70Percentage, null=False)
    al            = VariableFloatFieldMixin(model_variable=ArableLand, null=False)
    excal         = VariableFloatFieldMixin(model_variable=ExcessCalories, null=False)
    fert          = VariableFloatFieldMixin(model_variable=FertilizersProduction, null=False)
    rend          = VariableFloatFieldMixin(model_variable=AgricultureYield, null=False)
    falu          = VariableFloatFieldMixin(model_variable=PotentialArableLandProportion, null=False)
    urbanr        = VariableFloatFieldMixin(model_variable=UrbanPopulationPercentage, null=False)
    turbh         = VariableFloatFieldMixin(model_variable=UrbanizationRate, null=False)
    sepopr        = VariableFloatFieldMixin(model_variable=SecondaryLaborForcePercentage, null=False)
    houser        = VariableFloatFieldMixin(model_variable=HousesPerPersonPercentage, null=False)
    perxfl        = VariableFloatFieldMixin(model_variable=PeoplePerFamily, null=False)
    gnp           = VariableFloatFieldMixin(model_variable=GNP, null=False)
    gnpd_1        = VariableFloatFieldMixin(model_variable=GNPFoodSectorProportion, null=False)
    gnpd_2        = VariableFloatFieldMixin(model_variable=GNPHousingSectorProportion, null=False)
    gnpd_3        = VariableFloatFieldMixin(model_variable=GNPEducationSectorProportion, null=False)
    gnpd_4        = VariableFloatFieldMixin(model_variable=GNPOtherGoodsSectorProportion, null=False)
    gnpd_5        = VariableFloatFieldMixin(model_variable=GNPCapitalGoodsSectorProportion, null=False)

    def get_variables_information(self):
        fields_names    = [x.name for x in self._meta.get_fields() if isinstance(x, VariableFloatFieldMixin)]
        extra_info_dict = {field : getattr(self, field).info_as_dict() for field in fields_names}
        return extra_info_dict
    
    class Meta:
        unique_together = ('region_result', 'year')


# ADAPTAME
class GeneralParameters(models.Model):
    KSTOP = models.IntegerField(null=False, blank=True, default=42)


# ADAPTAME
class LAWMRunParameters(models.Model):
    general_parameters = models.ForeignKey(GeneralParameters, related_name="run_parameters", null=False, on_delete=models.CASCADE)
    simulation         = models.ForeignKey(LAWMSimulation   , related_name="run_parameters", null=False, on_delete=models.CASCADE)


# ADAPTAME
class RegionalParameters(models.Model):
    run_parameters = models.ForeignKey(LAWMRunParameters, related_name="regional_parameters", null=False, on_delete=models.CASCADE)
    region     = models.ForeignKey(LAWMRegion       , related_name="regional_parameters", null=False, on_delete=models.CASCADE)
    CALMX = models.IntegerField(null=False, blank=True, default=42)
