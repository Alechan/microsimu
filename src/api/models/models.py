from api.models.fields import *
from api.std_lib.lawm.parameters import *
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


class GeneralParameters(models.Model):
    simulation_stop      = ParameterIntegerField(model_parameter=SimulationStop          , null=False, blank=True)
    optimization_start   = ParameterIntegerField(model_parameter=OptimizationStart  , null=False, blank=True)
    payments_equilibrium = ParameterIntegerField(model_parameter=PaymentsEquilibrium, null=False, blank=True)
    fertilizer_cost      = ParameterFloatField(model_parameter=FertilizerCost     , null=False, blank=True)
    weight_constraint_1  = ParameterFloatField(model_parameter=WeightConstraint1  , null=False, blank=True)
    weight_constraint_2  = ParameterFloatField(model_parameter=WeightConstraint2  , null=False, blank=True)
    weight_constraint_3  = ParameterFloatField(model_parameter=WeightConstraint3  , null=False, blank=True)
    weight_constraint_4  = ParameterFloatField(model_parameter=WeightConstraint4  , null=False, blank=True)
    weight_constraint_5  = ParameterFloatField(model_parameter=WeightConstraint5  , null=False, blank=True)
    weight_constraint_6  = ParameterFloatField(model_parameter=WeightConstraint6  , null=False, blank=True)
    weight_constraint_7  = ParameterFloatField(model_parameter=WeightConstraint7  , null=False, blank=True)
    weight_constraint_8  = ParameterFloatField(model_parameter=WeightConstraint8  , null=False, blank=True)
    weight_constraint_9  = ParameterFloatField(model_parameter=WeightConstraint9  , null=False, blank=True)
    weight_constraint_10 = ParameterFloatField(model_parameter=WeightConstraint10 , null=False, blank=True)
    weight_constraint_11 = ParameterFloatField(model_parameter=WeightConstraint11 , null=False, blank=True)
    weight_constraint_12 = ParameterFloatField(model_parameter=WeightConstraint12 , null=False, blank=True)
    weight_constraint_13 = ParameterFloatField(model_parameter=WeightConstraint13 , null=False, blank=True)
    weight_constraint_14 = ParameterFloatField(model_parameter=WeightConstraint14 , null=False, blank=True)
    weight_constraint_15 = ParameterFloatField(model_parameter=WeightConstraint15 , null=False, blank=True)
    weight_constraint_16 = ParameterFloatField(model_parameter=WeightConstraint16 , null=False, blank=True)
    weight_constraint_17 = ParameterFloatField(model_parameter=WeightConstraint17 , null=False, blank=True)
    weight_constraint_18 = ParameterFloatField(model_parameter=WeightConstraint18 , null=False, blank=True)
    weight_constraint_19 = ParameterFloatField(model_parameter=WeightConstraint19 , null=False, blank=True)
    weight_constraint_20 = ParameterFloatField(model_parameter=WeightConstraint20 , null=False, blank=True)
    weight_constraint_21 = ParameterFloatField(model_parameter=WeightConstraint21 , null=False, blank=True)
    weight_constraint_22 = ParameterFloatField(model_parameter=WeightConstraint22 , null=False, blank=True)
    weight_constraint_23 = ParameterFloatField(model_parameter=WeightConstraint23 , null=False, blank=True)
    weight_constraint_24 = ParameterFloatField(model_parameter=WeightConstraint24 , null=False, blank=True)
    weight_constraint_25 = ParameterFloatField(model_parameter=WeightConstraint25 , null=False, blank=True)
    weight_constraint_26 = ParameterFloatField(model_parameter=WeightConstraint26 , null=False, blank=True)


# ADAPTAME
class LAWMRunParameters(models.Model):
    general_parameters = models.ForeignKey(GeneralParameters, related_name="run_parameters", null=False, on_delete=models.CASCADE)
    simulation         = models.ForeignKey(LAWMSimulation   , related_name="run_parameters", null=False, on_delete=models.CASCADE)



# ADAPTAME
class RegionalParameters(models.Model):
    run_parameters = models.ForeignKey(LAWMRunParameters, related_name="regional_parameters", null=False, on_delete=models.CASCADE)
    region     = models.ForeignKey(LAWMRegion       , related_name="regional_parameters", null=False, on_delete=models.CASCADE)
    CALMX = models.IntegerField(null=False, blank=True, default=42)
