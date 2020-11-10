from dataclasses import dataclass
from typing import Any

from api.std_lib.lawm.base_parameter import ModelRegionalParameter


@dataclass
class MaxCalories(ModelRegionalParameter):
    value: Any
    default       : dict  = (("developed", 3200), ("latinamerica", 3000), ("africa", 3000), ("asia", 3000))
    minimum       : float = 2600.0
    maximum       : float = 3200.0
    name          : str   = "Max calories"
    fortran_name  : str   = "CALMX(IB)"
    unit          : str   = "calories per day per person"
    description   : str   = "Maximum consumption of calories per day per person"


@dataclass
class MaxBuildCost(ModelRegionalParameter):
    value: Any
    default       : dict  = (("developed", 10), ("latinamerica", 7), ("africa", 7), ("asia", 7))
    minimum       : float = 5.0
    maximum       : float = 20.0
    name          : str   = "Max build cost"
    fortran_name  : str   = "COSMAX(IB)"
    unit          : str   = "US$ per m^2"
    description   : str   = "Maximum cost of the built square meter"


@dataclass
class TechProgressCoefficient1(ModelRegionalParameter):
    value         : Any
    default       : dict  = (("developed", 1.01), ("latinamerica", 1.01), ("africa", 1.01), ("asia", 1.01))
    minimum       : float = 1.0
    maximum       : float = 1.1
    name          : str   = "Tech progress coefficient 1"
    fortran_name  : str   = "GAMMA(IB,1)"
    unit          : str   = "None"
    description   : str   = "Coefficient of technological progress of Food Sector"


@dataclass
class TechProgressCoefficient2(ModelRegionalParameter):
    value         : Any
    default       : dict  = (("developed", 1.01), ("latinamerica", 1.01), ("africa", 1.01), ("asia", 1.01))
    minimum       : float = 1.0
    maximum       : float = 1.1
    name          : str   = "Tech progress coefficient 2"
    fortran_name  : str   = "GAMMA(IB,2)"
    unit          : str   = "None"
    description   : str   = "Coefficient of technological progress of Housing Sector"


@dataclass
class TechProgressCoefficient3(ModelRegionalParameter):
    value         : Any
    default       : dict  = (("developed", 1.005), ("latinamerica", 1.005), ("africa", 1.005), ("asia", 1.005))
    minimum       : float = 1.0
    maximum       : float = 1.1
    name          : str   = "Tech progress coefficient 3"
    fortran_name  : str   = "GAMMA(IB,3)"
    unit          : str   = "None"
    description   : str   = "Coefficient of technological progress of Education Sector"


@dataclass
class TechProgressCoefficient4(ModelRegionalParameter):
    value         : Any
    default       : dict  = (("developed", 1.01), ("latinamerica", 1.01), ("africa", 1.01), ("asia", 1.01))
    minimum       : float = 1.0
    maximum       : float = 1.1
    name          : str   = "Tech progress coefficient 4"
    fortran_name  : str   = "GAMMA(IB,4)"
    unit          : str   = "None"
    description   : str   = "Coefficient of technological progress of Other Goods Sector"


@dataclass
class TechProgressCoefficient5(ModelRegionalParameter):
    value         : Any
    default       : dict  = (("developed", 1.015), ("latinamerica", 1.015), ("africa", 1.015), ("asia", 1.015))
    minimum       : float = 1.0
    maximum       : float = 1.1
    name          : str   = "Tech progress coefficient 5"
    fortran_name  : str   = "GAMMA(IB,5)"
    unit          : str   = "None"
    description   : str   = "Coefficient of technological progress of Capital Goods Sector"


@dataclass
class TechProgressStop(ModelRegionalParameter):
    value         : Any
    default       : dict  = (("developed", 3000), ("latinamerica", 3000), ("africa", 3000), ("asia", 3000))
    minimum       : float = 1990.0
    maximum       : float = 3000.0
    name          : str   = "Tech progress stop"
    fortran_name  : str   = "KTECST(IB)"
    unit          : str   = "year"
    description   : str   = "Year at which technological progress stops"


@dataclass
class YearsForBuildingCostEquality(ModelRegionalParameter):
    value         : Any
    default       : dict  = (("developed", 40), ("latinamerica", 40), ("africa", 40), ("asia", 40))
    minimum       : float = 20.0
    maximum       : float = 100.0
    name          : str   = "Years for building cost equality"
    fortran_name  : str   = "NHCGAP(IB)"
    unit          : str   = "years"
    description   : str   = "Number of years (after basic needs are satisfied) in which the cost of " \
                            "building in developing countries is the same as in developed ones."


@dataclass
class YearsForHousingLevelEquality(ModelRegionalParameter):
    """
    Only used in regions Africa and Asia
    """
    value         : Any
    default       : dict = (("developed", 10), ("latinamerica", 10), ("africa", 20), ("asia", 20))
    minimum       : float = 10.0
    maximum       : float = 50.0
    name          : str = "Years for housing level equality"
    fortran_name  : str = "NQH34(IB)"
    unit          : str = "years"
    description   : str = "Only for regions Africa and Asia and ignored in others. Number or years in which Africa" \
                          " and Asia are supposed to reach the level of housing of Latin-America (values for 4 "\
                          " regions even though only 2 are used)."


@dataclass
class DesiredFoodStock(ModelRegionalParameter):
    value         : Any
    default       : dict  = (("developed", 365), ("latinamerica", 365), ("africa", 365), ("asia", 365))
    minimum       : float = 100.0
    maximum       : float = 730.0
    name          : str   = "Desired food stock"
    fortran_name  : str   = "NRESER(IB)"
    unit          : str   = "days"
    description   : str   = "Defines the desired food stock"


@dataclass
class YearsForSpacePerPersonEquality(ModelRegionalParameter):

    value         : Any
    default       : dict  = (("developed", 40), ("latinamerica", 40), ("africa", 40), ("asia", 40))
    minimum       : float = 10.0
    maximum       : float = 100.0
    name          : str   = "Years for space per person equality"
    fortran_name  : str   = "NSPGAP(IB)"
    unit          : str   = "years"
    description   : str   = "Number of years, after basic needs are satisfied, in which the space per person in " \
                            "developing countries reaches the value of the developed ones."


@dataclass
class MaxSpacePerPerson(ModelRegionalParameter):
    value         : Any
    default       : dict  = (("developed", 30), ("latinamerica", 30), ("africa", 30), ("asia", 30))
    minimum       : float = 10.0
    maximum       : float = 100.0
    name          : str   = "Max space per person"
    fortran_name  : str   = "SPAMAX(IB)"
    unit          : str   = "m^2"
    description   : str   = "Maximum space per person"


@dataclass
class DesiredSpacePerPerson(ModelRegionalParameter):
    value         : Any
    default       : dict  = (("developed", 30), ("latinamerica", 10), ("africa", 7), ("asia", 7))
    minimum       : float = 5.0
    maximum       : float = 50.0
    name          : str   = "Desired space per person"
    fortran_name  : str   = "SPXPER(IB)"
    unit          : str   = "m^2"
    description   : str   = "Desired space per person."


@dataclass
class MaxCapitalGoodsGNPProportion(ModelRegionalParameter):
    value         : Any
    default       : dict = (("developed", 0.25), ("latinamerica", 0.25), ("africa", 0.25), ("asia", 0.25))
    minimum       : float = 0.1
    maximum       : float = 0.35
    name          : str   = "Max capital goods GNP proportion"
    fortran_name  : str   = "UPTOIN(IB)"
    unit          : str   = "proportion"
    description   : str   = "Maximum proportion of the GNP allocated to Sector 5 (Capital Goods)"


