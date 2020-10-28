from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class ModelVariable:
    """
    A class representing variables of a model. By convention, each subclass
    (like Population(ModelVariable) should
      1. Put 'value: Any' first in the list of attributes
      2. For each of the other attributes (name, fortran_name, etc) it should specify
         its type again (str) and a default value. For example, 'name : str = "Population"
      3. Even though it's not necessary for correct execution, subclassify this class to
         point the reader to this description.
     """
    value       : Any
    name        : str
    fortran_name: str
    unit        : str
    description : str
    category    : str

    @classmethod
    def info_as_dict(cls):
        """
        Returns the variable information excluding the value attribute

        :return: a dictionary such as {name:"Population", "unit":"persons",...} - {"value": 423}
        """
        # Create an instance that with any value
        # noinspection PyArgumentList
        instance = cls(1)
        # Call the official dataclass asdict
        base_dict = asdict(instance)
        # Remove the value key
        del base_dict["value"]
        return base_dict


@dataclass
class Population(ModelVariable):
    value       : Any
    name        : str = "Population"
    fortran_name: str = "POP(IB)"
    unit        : str = "persons"
    description : str = "The total population."
    category    : str = "Demography"


@dataclass
class PopulationGrowth(ModelVariable):
    value       : Any
    name        : str = "Population growth"
    fortran_name: str = "POPR(IB)"
    unit        : str = "percentage"
    description : str = "The percentage of population growth from one year to the next."
    category    : str = "Demography"


@dataclass
class LifeExpectancy(ModelVariable):
    value       : Any
    name        : str = "Life expectancy"
    fortran_name: str = "EXLIFE(IB)"
    unit        : str = "years"
    description : str = "The life expectancy of the population."
    category    : str = "Demography"


@dataclass
class GrossMortality(ModelVariable):
    value       : Any
    name        : str = "Gross mortality"
    fortran_name: str = "GRMOR(IB)"
    unit        : str = "deaths per 1000 inhabitants"
    description : str = "The crude death rate calculated by 1000*deaths/pop."
    category    : str = "Demography"


@dataclass
class BirthRate(ModelVariable):
    value       : Any
    name        : str = "Birth rate"
    fortran_name: str = "BIRTHR(IB)"
    unit        : str = "births per 1000 per inhabitants"
    description : str = "The crude birth rate calculated by 1000*births/pop."
    category    : str = "Demography"


@dataclass
class ChildMortalityRate(ModelVariable):
    value       : Any
    name        : str = "Child mortality rate"
    fortran_name: str = "CHMOR(IB)"
    unit        : str = "child deaths per 1000 births"
    description : str = "The child death rate calculated by a complex formula."
    category    : str = "Demography"


@dataclass
class Calories(ModelVariable):
    value       : Any
    name        : str = "Calories"
    fortran_name: str = "CALOR(IB)"
    unit        : str = "calories per day per person"
    description : str = "The calories available per day to each person."
    category    : str = "Food sector"


@dataclass
class Proteins(ModelVariable):
    value       : Any
    name        : str = "Proteins"
    fortran_name: str = "PROT(IB)"
    unit        : str = "proteins per day per person"
    description : str = "The proteins available per day to each person."
    category    : str = "Food sector"


@dataclass
class HousesPerFamily(ModelVariable):
    value       : Any
    name        : str = "Houses per family"
    fortran_name: str = "HSEXFL(IB)"
    unit        : str = "houses per family"
    description : str = "The houses per family calculated by houses*(people_per_family/pop)."
    category    : str = "Housing sector"


@dataclass
class GNPPerPerson(ModelVariable):
    value       : Any
    name        : str = "GNP per person"
    fortran_name: str = "GNPXC(IB)"
    unit        : str = "US$ per person"
    description : str = "The Gross National Product per person calculated by GNP/pop."
    category    : str = "GNP"


@dataclass
class EnrolmentPercentage(ModelVariable):
    value       : Any
    name        : str = "Enrolment percentage"
    fortran_name: str = "ENROL(IB)"
    unit        : str = "percentage"
    description : str = "Percentage of population between 7 and 18 which is matriculated."
    category    : str = "Education sector"


@dataclass
class MatriculationPercentage(ModelVariable):
    value       : Any
    name        : str = "Matriculation percentage"
    fortran_name: str = "EDUCR(IB)"
    unit        : str = "percentage"
    description : str = "Percentage of population that is matriculated."
    category    : str = "Education sector"


@dataclass
class Pop11To70LaborForcePercentage(ModelVariable):
    value       : Any
    name        : str = "Percentage of population between ages 11 to 70 that is economically active."
    fortran_name: str = "EAPOPR(IB)"
    unit        : str = "percentage"
    description : str = "Rate of change of the fraction of the population which is economically active" \
                        " calculated by 100 * (labor_force_proportion * population)/pop_11_to_70 "
    category    : str = "Demography"


@dataclass
class TotalLaborForce(ModelVariable):
    value       : Any
    name        : str = "Total labor force"
    fortran_name: str = "TLF(IB)"
    unit        : str = "persons"
    description : str = "The size of the labor force."
    category    : str = "Labor force"


@dataclass
class LaborForceFoodSectorProportion(ModelVariable):
    value       : Any
    name        : str = "Labor force food sector proportion"
    fortran_name: str = "RLFD(1, IB)"
    unit        : str = "proportion"
    description : str = "The proportion of labor force corresponding to the food sector."
    category    : str = "Labor force"


@dataclass
class LaborForceHousingSectorProportion(ModelVariable):
    value       : Any
    name        : str = "Labor force housing sector proportion"
    fortran_name: str = "RLFD(2, IB)"
    unit        : str = "proportion"
    description : str = "The proportion of labor force corresponding to the housing sector."
    category    : str = "Labor force"


@dataclass
class LaborForceEducationSectorProportion(ModelVariable):
    value       : Any
    name        : str = "Labor force education sector proportion"
    fortran_name: str = "RLFD(3, IB)"
    unit        : str = "proportion"
    description : str = "The proportion of labor force corresponding to the education sector."
    category    : str = "Labor force"


@dataclass
class LaborForceOtherGoodsProportion(ModelVariable):
    value       : Any
    name        : str = "Labor force other goods sector proportion"
    fortran_name: str = "RLFD(4, IB)"
    unit        : str = "proportion"
    description : str = "The proportion of labor force corresponding to the other goods sector."
    category    : str = "Labor force"


@dataclass
class LaborForceCapitalGoodsSectorProportion(ModelVariable):
    value       : Any
    name        : str = "Labor force capital goods sector proportion"
    fortran_name: str = "RLFD(5, IB)"
    unit        : str = "proportion"
    description : str = "The proportion of labor force corresponding to the capital goods sector."
    category    : str = "Labor force"


@dataclass
class TotalCapital(ModelVariable):
    value       : Any
    name        : str = "Total capital"
    fortran_name: str = "CAPT(IB)"
    unit        : str = "US$"
    description : str = "The aggregated capital of all economic sectors."
    category    : str = "Capital"


@dataclass
class CapitalFoodSectorProportion(ModelVariable):
    value       : Any
    name        : str = "Capital food sector proportion"
    fortran_name: str = "CAPD(1, IB)"
    unit        : str = "proportion"
    description : str = "The proportion of capital corresponding to the food sector."
    category    : str = "Capital"


@dataclass
class CapitalHousingSectorProportion(ModelVariable):
    value       : Any
    name        : str = "Capital housing sector proportion"
    fortran_name: str = "CAPD(2, IB)"
    unit        : str = "proportion"
    description : str = "The proportion of capital corresponding to the housing sector."
    category    : str = "Capital"


@dataclass
class CapitalEducationSectorProportion(ModelVariable):
    value       : Any
    name        : str = "Capital education sector proportion"
    fortran_name: str = "CAPD(3, IB)"
    unit        : str = "proportion"
    description : str = "The proportion of capital corresponding to the education sector."
    category    : str = "Capital"


@dataclass
class CapitalOtherGoodsSectorProportion(ModelVariable):
    value       : Any
    name        : str = "Capital other goods sector proportion"
    fortran_name: str = "CAPD(4, IB)"
    unit        : str = "proportion"
    description : str = "The proportion of capital corresponding to the other goods sector."
    category    : str = "Capital"


@dataclass
class CapitalCapitalGoodsSectorProportion(ModelVariable):
    value       : Any
    name        : str = "Capital capital goods sector proportion"
    fortran_name: str = "CAPD(5, IB)"
    unit        : str = "proportion"
    description : str = "The proportion of capital corresponding to the capital goods sector."
    category    : str = "Capital"


@dataclass
class Pop0to5Percentage(ModelVariable):
    value       : Any
    name        : str = "Population 0 to 5 percentage"
    fortran_name: str = "PYRAM_perc(1,IB)"
    unit        : str = "percentage"
    description : str = "The percentage of the population falling in age group 0 to 5."
    category    : str = "Demography"


@dataclass
class Pop6to17Percentage(ModelVariable):
    value       : Any
    name        : str = "Population 6 to 17 percentage"
    fortran_name: str = "PYRAM_perc(2,IB)"
    unit        : str = "percentage"
    description : str = "The percentage of the population falling in age group 6 to 17."
    category    : str = "Demography"


@dataclass
class Pop11to70Percentage(ModelVariable):
    value       : Any
    name        : str = "Population 11 to 70 percentage"
    fortran_name: str = "PYRAM_perc(3,IB)"
    unit        : str = "percentage"
    description : str = "The percentage of the population falling in age group 11 to 70."
    category    : str = "Demography"


@dataclass
class ArableLand(ModelVariable):
    value       : Any
    name        : str = "Arable land"
    fortran_name: str = "AL(IB)"
    unit        : str = "1000 ha"
    description : str = "The size of the cultivated arable land. "
    category    : str = "Food sector"


@dataclass
class ExcessCalories(ModelVariable):
    value       : Any
    name        : str = "Excess Calories"
    fortran_name: str = "EXCAL(IB)"
    unit        : str = "calories per day per person"
    description : str = "The amount of calories above the max calories per day per person."
    category    : str = "Food sector"


@dataclass
class FertilizersProduction(ModelVariable):
    value       : Any
    name        : str = "Fertilizers production"
    fortran_name: str = "FERT(IB)"
    unit        : str = "1000 tons"
    description : str = "The production of fertilizers."
    category    : str = "Food sector"


@dataclass
class AgricultureYield(ModelVariable):
    value       : Any
    name        : str = "Agriculture yield"
    fortran_name: str = "REND(IB)"
    unit        : str = "tons per ha"
    description : str = "The agriculture yield per hectare measured in tons."
    category    : str = "Food sector"


@dataclass
class PotentialArableLandProportion(ModelVariable):
    value       : Any
    name        : str = "Potential arable land proportion"
    fortran_name: str = "FALU(IB)"
    unit        : str = "proportion"
    description : str = "Proportion of potentially arable land that is not cultivated calculated by" \
                        "1 - arable_land/total_potential_arable_land . "
    category    : str = "Food sector"


@dataclass
class UrbanPopulationPercentage(ModelVariable):
    value       : Any
    name        : str = "Urban population percentage"
    fortran_name: str = "URBANR(IB)"
    unit        : str = "percentage"
    description : str = "The percentage of the population living in cities"
    category    : str = "Demography"


@dataclass
class UrbanizationRate(ModelVariable):
    value       : Any
    name        : str = "Urbanization rate"
    fortran_name: str = "TURBH(IB)"
    unit        : str = "persons per ha"
    description : str = "The urbanization rate calculated by " \
                        "max(0.,(population_this_year-population_prev_year)/max_pop_density_per_ha"
    category    : str = "Demography"


@dataclass
class SecondaryLaborForcePercentage(ModelVariable):
    value       : Any
    name        : str = "Secondary laborForce percentage"
    fortran_name: str = "SEPOPR(IB)"
    unit        : str = "percentage"
    description : str = "The percentage of secondary labor force calculated by" \
                        "100*(labor_force_cap_goods_sec_proportion + " \
                        "other_goods_sec_secondary_labor_force_fraction * labor_force_other_goods_sec_proportion)"
    category    : str = "Labor force"


@dataclass
class HousesPerPersonPercentage(ModelVariable):
    value       : Any
    name        : str = "Houses per person percentage"
    fortran_name: str = "HOUSER(IB)"
    unit        : str = "percentage"
    description : str = "The percentage of houses per population calculated by 100*houses/pop."
    category    : str = "Housing sector"


@dataclass
class PeoplePerFamily(ModelVariable):
    value       : Any
    name        : str = "People per family"
    fortran_name: str = "PERXFL(IB)"
    unit        : str = "persons"
    description : str = "The number of people per family."
    category    : str = "Demography"


@dataclass
class GNP(ModelVariable):
    value       : Any
    name        : str = "GNP"
    fortran_name: str = "GNP(IB)"
    unit        : str = "US$"
    description : str = "The aggregated Gross National Product of all economic sectors."
    category    : str = "GNP"


@dataclass
class GNPFoodSectorProportion(ModelVariable):
    value       : Any
    name        : str = "GNP food sector proportion"
    fortran_name: str = "GNPD(1, IB)"
    unit        : str = "proportion"
    description : str = "The proportion of Gross National Product corresponding to the food sector."
    category    : str = "GNP"


@dataclass
class GNPHousingSectorProportion(ModelVariable):
    value       : Any
    name        : str = "GNP housing sector proportion"
    fortran_name: str = "GNPD(2, IB)"
    unit        : str = "proportion"
    description : str = "The proportion of Gross National Product corresponding to the housing sector."
    category    : str = "GNP"


@dataclass
class GNPEducationSectorProportion(ModelVariable):
    value       : Any
    name        : str = "GNP education sector proportion"
    fortran_name: str = "GNPD(3, IB)"
    unit        : str = "proportion"
    description : str = "The proportion of Gross National Product corresponding to the education sector."
    category    : str = "GNP"


@dataclass
class GNPOtherGoodsSectorProportion(ModelVariable):
    value       : Any
    name        : str = "GNP other goods sector proportion"
    fortran_name: str = "GNPD(4, IB)"
    unit        : str = "proportion"
    description : str = "The proportion of Gross National Product corresponding to the other" \
                        " goods sector."
    category    : str = "GNP"


@dataclass
class GNPCapitalGoodsSectorProportion(ModelVariable):
    value       : Any
    name        : str = "GNP capital goods sector proportion"
    fortran_name: str = "GNPD(5, IB)"
    unit        : str = "proportion"
    description : str = "The proportion of Gross National Product corresponding to the capital" \
                        " goods sector."
    category    : str = "GNP"
