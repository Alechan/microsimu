from django.db import models

from api.models.fields import VariableFloatField
from api.std_lib.lawm.variables import *


class LAWMRegion(models.Model):
    name = models.CharField(max_length=100, primary_key=True)


class LAWMSimulation(models.Model):
    created = models.DateTimeField(auto_now_add=True)


class LAWMRegionResult(models.Model):
    simulation = models.ForeignKey(LAWMSimulation, related_name="region_results", null=False, on_delete=models.CASCADE)
    region     = models.OneToOneField(LAWMRegion    , related_name="region_result", null=False, on_delete=models.CASCADE)

    unique_together = ('simulation', 'year')

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
    pop           = VariableFloatField(model_variable=Population, null=False)
    popr          = VariableFloatField(model_variable=PopulationGrowth, null=False)
    exlife        = VariableFloatField(model_variable=LifeExpectancy, null=False)
    grmor         = VariableFloatField(model_variable=GrossMortality, null=False)
    birthr        = VariableFloatField(model_variable=BirthRate, null=False)
    chmor         = VariableFloatField(model_variable=ChildMortalityRate, null=False)
    calor         = VariableFloatField(model_variable=Calories, null=False)
    prot          = VariableFloatField(model_variable=Proteins, null=False)
    hsexfl        = VariableFloatField(model_variable=HousesPerFamily, null=False)
    gnpxc         = VariableFloatField(model_variable=GNPPerPerson, null=False)
    enrol         = VariableFloatField(model_variable=EnrolmentPercentage, null=False)
    educr         = VariableFloatField(model_variable=MatriculationPercentage, null=False)
    eapopr        = VariableFloatField(model_variable=Pop11To70LaborForcePercentage, null=False)
    tlf           = VariableFloatField(model_variable=TotalLaborForce, null=False)
    rlfd_1        = VariableFloatField(model_variable=LaborForceFoodSectorProportion, null=False)
    rlfd_2        = VariableFloatField(model_variable=LaborForceHousingSectorProportion, null=False)
    rlfd_3        = VariableFloatField(model_variable=LaborForceEducationSectorProportion, null=False)
    rlfd_4        = VariableFloatField(model_variable=LaborForceOtherGoodsProportion, null=False)
    rlfd_5        = VariableFloatField(model_variable=LaborForceCapitalGoodsSectorProportion, null=False)
    capt          = VariableFloatField(model_variable=TotalCapital, null=False)
    capd_1        = VariableFloatField(model_variable=CapitalFoodSectorProportion, null=False)
    capd_2        = VariableFloatField(model_variable=CapitalHousingSectorProportion, null=False)
    capd_3        = VariableFloatField(model_variable=CapitalEducationSectorProportion, null=False)
    capd_4        = VariableFloatField(model_variable=CapitalOtherGoodsSectorProportion, null=False)
    capd_5        = VariableFloatField(model_variable=CapitalCapitalGoodsSectorProportion, null=False)
    _0_5          = VariableFloatField(model_variable=Pop0to5Percentage, null=False)
    _6_17         = VariableFloatField(model_variable=Pop6to17Percentage, null=False)
    _11_70        = VariableFloatField(model_variable=Pop11to70Percentage, null=False)
    al            = VariableFloatField(model_variable=ArableLand, null=False)
    excal         = VariableFloatField(model_variable=ExcessCalories, null=False)
    fert          = VariableFloatField(model_variable=FertilizersProduction, null=False)
    rend          = VariableFloatField(model_variable=AgricultureYield, null=False)
    falu          = VariableFloatField(model_variable=PotentialArableLandProportion, null=False)
    urbanr        = VariableFloatField(model_variable=UrbanPopulationPercentage, null=False)
    turbh         = VariableFloatField(model_variable=UrbanizationRate, null=False)
    sepopr        = VariableFloatField(model_variable=SecondaryLaborForcePercentage, null=False)
    houser        = VariableFloatField(model_variable=HousesPerPersonPercentage, null=False)
    perxfl        = VariableFloatField(model_variable=PeoplePerFamily, null=False)
    gnp           = VariableFloatField(model_variable=GNP, null=False)
    gnpd_1        = VariableFloatField(model_variable=GNPFoodSectorProportion, null=False)
    gnpd_2        = VariableFloatField(model_variable=GNPHousingSectorProportion, null=False)
    gnpd_3        = VariableFloatField(model_variable=GNPEducationSectorProportion, null=False)
    gnpd_4        = VariableFloatField(model_variable=GNPOtherGoodsSectorProportion, null=False)
    gnpd_5        = VariableFloatField(model_variable=GNPCapitalGoodsSectorProportion, null=False)

    def get_variables_information(self):
        fields_names    = [x.name for x in self._meta.get_fields() if isinstance(x, VariableFloatField)]
        extra_info_dict = {field : getattr(self, field).info_as_dict() for field in fields_names}
        return extra_info_dict
    
    class Meta:
        unique_together = ('region_result', 'year')
