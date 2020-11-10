from dataclasses import dataclass
from typing import Any

from api.std_lib.lawm.base_parameter import ModelGeneralParameter


@dataclass
class SimulationStop(ModelGeneralParameter):
    value       : Any
    default     : int = 2000
    minimum     : int = 1990
    maximum     : int = 2050
    name        : str = "Simulation stop"
    fortran_name: str = "KSTOP"
    unit        : str = "year"
    description : str = "The last year of the simulation."


@dataclass
class OptimizationStart(ModelGeneralParameter):
    value       : Any
    default     : int = 1980
    minimum     : int = 1980
    maximum     : int = 2050
    name        : str = "Simulation stop"
    fortran_name: str = "KPROJ"
    unit        : str = "year"
    description : str = "The year when the Optimization Phase should start."


@dataclass
class PaymentsEquilibrium(ModelGeneralParameter):
    value       : Any
    default     : int = 2000
    minimum     : int = 1990
    maximum     : int = 2050
    name        : str = "Payments equilibrium"
    fortran_name: str = "KTRADE"
    unit        : str = "year"
    description : str = "Year at which the balance of payments reaches the equilibrium (optimization_start <= " \
                        "BalanceOfPaymentsEquilibrium<= simulation_stop)."


@dataclass
class FertilizerCost(ModelGeneralParameter):
    value       : Any
    default     : float = 769230.8
    minimum     : float = 1
    maximum     : float = None
    name        : str = "Fertilizer cost"
    fortran_name: str = "FCOST"
    unit        : str = "US$ per tonne"
    description : str = "Cost of one tonne of fertilizer"


@dataclass
class WeightConstraint1(ModelGeneralParameter):
    value       : Any
    default     : float = 6.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 1"
    fortran_name: str = "WTH(1)"
    unit        : str = "None"
    description : str = "CONS(1)  the capital allocated to investment should increase"


@dataclass
class WeightConstraint2(ModelGeneralParameter):
    value       : Any
    default     : float = 8.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 2"
    fortran_name: str = "WTH(2)"
    unit        : str = "None"
    description : str = "CONS(2)  the GNP allocated to consumption should not decrease in more than 2% per year"


@dataclass
class WeightConstraint3(ModelGeneralParameter):
    value       : Any
    default     : float = 6.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 3"
    fortran_name: str = "WTH(3)"
    unit        : str = "None"
    description : str = "CONS(3)  The GNP allocated to consumption should not fall below 45%"


@dataclass
class WeightConstraint4(ModelGeneralParameter):
    value       : Any
    default     : float = 6.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 4"
    fortran_name: str = "WTH(4)"
    unit        : str = "None"
    description : str = "CONS(4)  Only active if CONS(3) fails"


@dataclass
class WeightConstraint5(ModelGeneralParameter):
    value       : Any
    default     : float = 6.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 5"
    fortran_name: str = "WTH(5)"
    unit        : str = "None"
    description : str = "CONS(5)  The labor force allocated to the investment sector should increase"


@dataclass
class WeightConstraint6(ModelGeneralParameter):
    value       : Any
    default     : float = 6.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 6"
    fortran_name: str = "WTH(6)"
    unit        : str = "None"
    description : str = "CONS(6)  Education should grow at least 3% per year"


@dataclass
class WeightConstraint7(ModelGeneralParameter):
    value       : Any
    default     : float = 4.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 7"
    fortran_name: str = "WTH(7)"
    unit        : str = "None"
    description : str = "CONS(7)  Fraction of families with a suitable home should increase and if Education and " \
                        "Calories reached the maximum they should grow at least 1.5% per year "


@dataclass
class WeightConstraint8(ModelGeneralParameter):
    value       : Any
    default     : float = 4.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 8"
    fortran_name: str = "WTH(8)"
    unit        : str = "None"
    description : str = "CONS(8)  The rate of investment should increase at least 2% per year"


@dataclass
class WeightConstraint9(ModelGeneralParameter):
    value       : Any
    default     : float = 6.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 9"
    fortran_name: str = "WTH(9)"
    unit        : str = "None"
    description : str = "CONS(9)  Only for block1: GNP allocated to sector 1 should increase"


@dataclass
class WeightConstraint10(ModelGeneralParameter):
    value       : Any
    default     : float = 6.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 10"
    fortran_name: str = "WTH(10)"
    unit        : str = "None"
    description : str = "CONS(10) The GNP allocated to consumption should not be lower than the value when " \
                        "optimization starts "


@dataclass
class WeightConstraint11(ModelGeneralParameter):
    value       : Any
    default     : float = 6.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 11"
    fortran_name: str = "WTH(11)"
    unit        : str = "None"
    description : str = "CONS(11) Education should increase (see CONS(6)) "


@dataclass
class WeightConstraint12(ModelGeneralParameter):
    value       : Any
    default     : float = 2.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 12"
    fortran_name: str = "WTH(12)"
    unit        : str = "None"
    description : str = "CONS(12) Fraction of families with a suitable home should increase (see CONS(7)) and if too " \
                        "small it should grow at least 1 percent per year "


@dataclass
class WeightConstraint13(ModelGeneralParameter):
    value       : Any
    default     : float = 4.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 13"
    fortran_name: str = "WTH(13)"
    unit        : str = "None"
    description : str = "CONS(13) The labor force allocated to the investment sector should be within its lower and " \
                        "upper bounds "


@dataclass
class WeightConstraint14(ModelGeneralParameter):
    value       : Any
    default     : float = 4.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 14"
    fortran_name: str = "WTH(14)"
    unit        : str = "None"
    description : str = "CONS(14) It complements CONS(13) when basic needs are satisfied"


@dataclass
class WeightConstraint15(ModelGeneralParameter):
    value       : Any
    default     : float = 7.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 15"
    fortran_name: str = "WTH(15)"
    unit        : str = "None"
    description : str = "CONS(15) The labor force defined by optimization should not increase in regard to the " \
                        "starting value "


@dataclass
class WeightConstraint16(ModelGeneralParameter):
    value       : Any
    default     : float = 4.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 16"
    fortran_name: str = "WTH(16)"
    unit        : str = "None"
    description : str = "CONS(16) The capital allocated to the investment sector should increase"


@dataclass
class WeightConstraint17(ModelGeneralParameter):
    value       : Any
    default     : float = 4.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 17"
    fortran_name: str = "WTH(17)"
    unit        : str = "None"
    description : str = "CONS(17) As CONS(16) but when basic needs are satisfied "


@dataclass
class WeightConstraint18(ModelGeneralParameter):
    value       : Any
    default     : float = 4.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 18"
    fortran_name: str = "WTH(18)"
    unit        : str = "None"
    description : str = "CONS(18) The GNP allocated to investment should increase"


@dataclass
class WeightConstraint19(ModelGeneralParameter):
    value       : Any
    default     : float = 8.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 19"
    fortran_name: str = "WTH(19)"
    unit        : str = "None"
    description : str = "CONS(19) If GNP per capita exceeds 4500 U$S it should not grow more than 3% per year"


@dataclass
class WeightConstraint20(ModelGeneralParameter):
    value       : Any
    default     : float = 6.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 20"
    fortran_name: str = "WTH(20)"
    unit        : str = "None"
    description : str = "CONS(20) Calories per capita should not exceed its upper bound"


@dataclass
class WeightConstraint21(ModelGeneralParameter):
    value       : Any
    default     : float = 4.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 21"
    fortran_name: str = "WTH(21)"
    unit        : str = "None"
    description : str = "CONS(21) The maximum of daily calories should exceed half the the excess of calories"


@dataclass
class WeightConstraint22(ModelGeneralParameter):
    value       : Any
    default     : float = 6.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 22"
    fortran_name: str = "WTH(22)"
    unit        : str = "None"
    description : str = "CONS(22) Daily calories should increase"


@dataclass
class WeightConstraint23(ModelGeneralParameter):
    value       : Any
    default     : float = 8.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 23"
    fortran_name: str = "WTH(23)"
    unit        : str = "None"
    description : str = "CONS(23) Education should not grow beyond its upper bound during the optimization phase "


@dataclass
class WeightConstraint24(ModelGeneralParameter):
    value       : Any
    default     : float = 6.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 24"
    fortran_name: str = "WTH(24)"
    unit        : str = "None"
    description : str = "CONS(24) The fraction of families with a suitable house should increase"


@dataclass
class WeightConstraint25(ModelGeneralParameter):
    value       : Any
    default     : float = 2.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 25"
    fortran_name: str = "WTH(25)"
    unit        : str = "None"
    description : str = "CONS(25) The fraction of families with a suitable house should not be higher than 1.5 but" \
                        " if calories  or education did not reach their optimum values the upper bound is 1 "


@dataclass
class WeightConstraint26(ModelGeneralParameter):
    value       : Any
    default     : float = 1.0
    minimum     : float = 1
    maximum     : float = 14
    name        : str = "Weight Constraint 26"
    fortran_name: str = "WTH(26)"
    unit        : str = "None"
    description : str = "CONS(26) Life expectancy should increase"
