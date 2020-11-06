from api.models.fields import *
from api.std_lib.lawm.general_parameters import *
from api.std_lib.lawm.regional_parameters import *

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
    simulation_stop      = ParameterIntegerField(model_parameter=SimulationStop     , use_parameter_default=True, null=False, blank=True)
    optimization_start   = ParameterIntegerField(model_parameter=OptimizationStart  , use_parameter_default=True, null=False, blank=True)
    payments_equilibrium = ParameterIntegerField(model_parameter=PaymentsEquilibrium, use_parameter_default=True, null=False, blank=True)
    fertilizer_cost      = ParameterFloatField(model_parameter=FertilizerCost       , use_parameter_default=True, null=False, blank=True)
    weight_constraint_1  = ParameterFloatField(model_parameter=WeightConstraint1    , use_parameter_default=True, null=False, blank=True)
    weight_constraint_2  = ParameterFloatField(model_parameter=WeightConstraint2    , use_parameter_default=True, null=False, blank=True)
    weight_constraint_3  = ParameterFloatField(model_parameter=WeightConstraint3    , use_parameter_default=True, null=False, blank=True)
    weight_constraint_4  = ParameterFloatField(model_parameter=WeightConstraint4    , use_parameter_default=True, null=False, blank=True)
    weight_constraint_5  = ParameterFloatField(model_parameter=WeightConstraint5    , use_parameter_default=True, null=False, blank=True)
    weight_constraint_6  = ParameterFloatField(model_parameter=WeightConstraint6    , use_parameter_default=True, null=False, blank=True)
    weight_constraint_7  = ParameterFloatField(model_parameter=WeightConstraint7    , use_parameter_default=True, null=False, blank=True)
    weight_constraint_8  = ParameterFloatField(model_parameter=WeightConstraint8    , use_parameter_default=True, null=False, blank=True)
    weight_constraint_9  = ParameterFloatField(model_parameter=WeightConstraint9    , use_parameter_default=True, null=False, blank=True)
    weight_constraint_10 = ParameterFloatField(model_parameter=WeightConstraint10   , use_parameter_default=True, null=False, blank=True)
    weight_constraint_11 = ParameterFloatField(model_parameter=WeightConstraint11   , use_parameter_default=True, null=False, blank=True)
    weight_constraint_12 = ParameterFloatField(model_parameter=WeightConstraint12   , use_parameter_default=True, null=False, blank=True)
    weight_constraint_13 = ParameterFloatField(model_parameter=WeightConstraint13   , use_parameter_default=True, null=False, blank=True)
    weight_constraint_14 = ParameterFloatField(model_parameter=WeightConstraint14   , use_parameter_default=True, null=False, blank=True)
    weight_constraint_15 = ParameterFloatField(model_parameter=WeightConstraint15   , use_parameter_default=True, null=False, blank=True)
    weight_constraint_16 = ParameterFloatField(model_parameter=WeightConstraint16   , use_parameter_default=True, null=False, blank=True)
    weight_constraint_17 = ParameterFloatField(model_parameter=WeightConstraint17   , use_parameter_default=True, null=False, blank=True)
    weight_constraint_18 = ParameterFloatField(model_parameter=WeightConstraint18   , use_parameter_default=True, null=False, blank=True)
    weight_constraint_19 = ParameterFloatField(model_parameter=WeightConstraint19   , use_parameter_default=True, null=False, blank=True)
    weight_constraint_20 = ParameterFloatField(model_parameter=WeightConstraint20   , use_parameter_default=True, null=False, blank=True)
    weight_constraint_21 = ParameterFloatField(model_parameter=WeightConstraint21   , use_parameter_default=True, null=False, blank=True)
    weight_constraint_22 = ParameterFloatField(model_parameter=WeightConstraint22   , use_parameter_default=True, null=False, blank=True)
    weight_constraint_23 = ParameterFloatField(model_parameter=WeightConstraint23   , use_parameter_default=True, null=False, blank=True)
    weight_constraint_24 = ParameterFloatField(model_parameter=WeightConstraint24   , use_parameter_default=True, null=False, blank=True)
    weight_constraint_25 = ParameterFloatField(model_parameter=WeightConstraint25   , use_parameter_default=True, null=False, blank=True)
    weight_constraint_26 = ParameterFloatField(model_parameter=WeightConstraint26   , use_parameter_default=True, null=False, blank=True)

    @classmethod
    def get_metadata(cls):
        all_fields      = cls._meta.get_fields()
        relevant_fields = [f for f in all_fields if isinstance(f, BaseParameterField)]
        extra_info_dict = {f.name : f.get_metadata() for f in relevant_fields}
        return extra_info_dict


class LAWMRunParameters(models.Model):
    general_parameters = models.ForeignKey(GeneralParameters, related_name="run_parameters", null=False, on_delete=models.CASCADE)
    simulation         = models.ForeignKey(LAWMSimulation   , related_name="run_parameters", null=False, on_delete=models.CASCADE)

    @classmethod
    def get_metadata(cls):
        return {
            "general" : GeneralParameters.get_metadata(),
            "regional": RegionalParameters.get_metadata(),
        }


class RegionalParameters(models.Model):
    run_parameters = models.ForeignKey(LAWMRunParameters, related_name="regional_parameters", null=False, blank=True, on_delete=models.CASCADE)
    region         = models.ForeignKey(LAWMRegion       , related_name="regional_parameters", null=False, blank=True, on_delete=models.CASCADE)
    max_calories            = ParameterFloatField(model_parameter   = MaxCalories                     , null=False , blank=True)
    max_build_cost          = ParameterFloatField(model_parameter   = MaxBuildCost                   , null=False , blank=True)
    tech_prog_coeff_1       = ParameterFloatField(model_parameter   = TechProgressCoefficient1       , null=False , blank=True)
    tech_prog_coeff_2       = ParameterFloatField(model_parameter   = TechProgressCoefficient2       , null=False , blank=True)
    tech_prog_coeff_3       = ParameterFloatField(model_parameter   = TechProgressCoefficient3       , null=False , blank=True)
    tech_prog_coeff_4       = ParameterFloatField(model_parameter   = TechProgressCoefficient4       , null=False , blank=True)
    tech_prog_coeff_5       = ParameterFloatField(model_parameter   = TechProgressCoefficient5       , null=False , blank=True)
    tech_prog_stop          = ParameterFloatField(model_parameter   = TechProgressStop               , null=False , blank=True)
    years_building_cost_eq  = ParameterIntegerField(model_parameter = YearsForBuildingCostEquality   , null=False , blank=True)
    years_housing_level_eq  = ParameterIntegerField(model_parameter = YearsForHousingLevelEquality   , null=False , blank=True)
    desired_food_stock      = ParameterFloatField(model_parameter   = DesiredFoodStock               , null=False , blank=True)
    years_space_p_person_eq = ParameterIntegerField(model_parameter = YearsForSpacePerPersonEquality , null=False , blank=True)
    max_space_p_person      = ParameterFloatField(model_parameter   = MaxSpacePerPerson              , null=False , blank=True)
    desired_space_p_person  = ParameterFloatField(model_parameter   = DesiredSpacePerPerson          , null=False , blank=True)
    max_sec_5_gnp_propor    = ParameterFloatField(model_parameter   = MaxCapitalGoodsGNPProportion   , null=False , blank=True)

    @classmethod
    def new_with_defaults_for_region(cls, run_parameters, region):
        """
        Instantiates the object but DOESN'T save to DB
        :param region_name:
        :return: a python object not saved to DB
        """
        region_name = region.name
        partial_creation_kwargs = cls.get_defaults_for_region(region_name)
        creation_kwargs = partial_creation_kwargs.copy()
        creation_kwargs["run_parameters"] = run_parameters
        creation_kwargs["region"]         = region
        return cls(**creation_kwargs)

    @classmethod
    def get_defaults_for_region(cls, region_name):
        all_fields = cls._meta.get_fields()
        relevant_fields = [f for f in all_fields if isinstance(f, BaseParameterField)]
        partial_creation_kwargs = {f.name: f.get_defaults_for_region(region_name) for f in relevant_fields}
        return partial_creation_kwargs

    @classmethod
    def get_metadata(cls):
        all_fields      = cls._meta.get_fields()
        relevant_fields = [f for f in all_fields if isinstance(f, BaseParameterField)]
        extra_info_dict = {f.name : f.get_metadata() for f in relevant_fields}
        return extra_info_dict

    class Meta:
        unique_together = ('run_parameters', 'region')
