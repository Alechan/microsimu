from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class ModelParameter:
    """
    A class representing parameters of a model. By convention, each subclass
    (like SimulationStop(ModelParameter) should
      1. Put 'value: Any' first in the list of attributes
      2. For each of the other attributes (name, fortran_name, etc) it should specify
         its type again (str) and a default value. For example, 'name : str = "Population"
      3. Even though it's not necessary for correct execution, subclassify this class to
         point the reader to this description.
     """
    value       : Any
    default     : Any
    minimum     : Any
    maximum     : Any
    name        : str
    fortran_name: str
    unit        : str
    description : str

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
class SimulationStop:
    value       : Any
    default     : int = 2000
    minimum     : int = 1990
    maximum     : int = 2050
    name        : str = "Simulation stop"
    fortran_name: str = "KSTOP(IB)"
    unit        : str = "year"
    description : str = "The last year of the simulation."


@dataclass
class OptimizationStart:
    value       : Any
    default     : int = 1980
    minimum     : int = 1980
    maximum     : int = 2050
    name        : str = "Simulation stop"
    fortran_name: str = "KPROJ(IB)"
    unit        : str = "year"
    description : str = "The year when the Optimization Phase should start."


@dataclass
class PaymentsEquilibrium:
    value       : Any
    default     : int = 2000
    minimum     : int = 1990
    maximum     : int = 2050
    name        : str = "Payments equilibrium"
    fortran_name: str = "KTRADE(IB)"
    unit        : str = "year"
    description : str = "Year at which the balance of payments reaches the equilibrium (optimization_start <= " \
                        "BalanceOfPaymentsEquilibrium<= simulation_stop)."


@dataclass
class FertilizerCost:
    value       : Any
    default     : float = 769230.8
    minimum     : float = 1
    maximum     : float = None
    name        : str = "Fertilizer cost"
    fortran_name: str = "FCOST(IB)"
    unit        : str = "US$ per tonne"
    description : str = "Cost of one tonne of fertilizer"


@dataclass
class WeightConstraint1:
    value       : Any
    default     : float = 6.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 1"
    fortran_name: str = "WTH(1)"
    unit        : str = "None"
    description : str = "CONS(1)  the capital allocated to investment should increase"


@dataclass
class WeightConstraint2:
    value       : Any
    default     : float = 8.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 2"
    fortran_name: str = "WTH(2)"
    unit        : str = "None"
    description : str = "CONS(2)  the GNP allocated to consumption should not decrease in more than 2% per year"


@dataclass
class WeightConstraint3:
    value       : Any
    default     : float = 6.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 3"
    fortran_name: str = "WTH(3)"
    unit        : str = "None"
    description : str = "CONS(3)  The GNP allocated to consumption should not fall below 45%"


@dataclass
class WeightConstraint4:
    value       : Any
    default     : float = 6.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 4"
    fortran_name: str = "WTH(4)"
    unit        : str = "None"
    description : str = "CONS(4)  Only active if CONS(3) fails"


@dataclass
class WeightConstraint5:
    value       : Any
    default     : float = 6.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 5"
    fortran_name: str = "WTH(5)"
    unit        : str = "None"
    description : str = "CONS(5)  The labor force allocated to the investment sector should increase"


@dataclass
class WeightConstraint6:
    value       : Any
    default     : float = 6.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 6"
    fortran_name: str = "WTH(6)"
    unit        : str = "None"
    description : str = "CONS(6)  Education should grow at least 3% per year"


@dataclass
class WeightConstraint7:
    value       : Any
    default     : float = 4.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 7"
    fortran_name: str = "WTH(7)"
    unit        : str = "None"
    description : str = "CONS(7)  Fraction of families with a suitable home should increase and if Education and " \
                        "Calories reached the maximum they should grow at least 1.5% per year "


@dataclass
class WeightConstraint8:
    value       : Any
    default     : float = 4.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 8"
    fortran_name: str = "WTH(8)"
    unit        : str = "None"
    description : str = "CONS(8)  The rate of investment should increase at least 2% per year"


@dataclass
class WeightConstraint9:
    value       : Any
    default     : float = 6.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 9"
    fortran_name: str = "WTH(9)"
    unit        : str = "None"
    description : str = "CONS(9)  Only for block1: GNP allocated to sector 1 should increase"


@dataclass
class WeightConstraint10:
    value       : Any
    default     : float = 6.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 10"
    fortran_name: str = "WTH(10)"
    unit        : str = "None"
    description : str = "CONS(10) The GNP allocated to consumption should not be lower than the value when " \
                        "optimization starts "


@dataclass
class WeightConstraint11:
    value       : Any
    default     : float = 6.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 11"
    fortran_name: str = "WTH(11)"
    unit        : str = "None"
    description : str = "CONS(11) Education should increase (see CONS(6)) "


@dataclass
class WeightConstraint12:
    value       : Any
    default     : float = 2.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 12"
    fortran_name: str = "WTH(12)"
    unit        : str = "None"
    description : str = "CONS(12) Fraction of families with a suitable home should increase (see CONS(7)) and if too " \
                        "small it should grow at least 1 percent per year "


@dataclass
class WeightConstraint13:
    value       : Any
    default     : float = 4.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 13"
    fortran_name: str = "WTH(13)"
    unit        : str = "None"
    description : str = "CONS(13) The labor force allocated to the investment sector should be within its lower and " \
                        "upper bounds "


@dataclass
class WeightConstraint14:
    value       : Any
    default     : float = 4.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 14"
    fortran_name: str = "WTH(14)"
    unit        : str = "None"
    description : str = "CONS(14) It complements CONS(13) when basic needs are satisfied"


@dataclass
class WeightConstraint15:
    value       : Any
    default     : float = 7.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 15"
    fortran_name: str = "WTH(15)"
    unit        : str = "None"
    description : str = "CONS(15) The labor force defined by optimization should not increase in regard to the " \
                        "starting value "


@dataclass
class WeightConstraint16:
    value       : Any
    default     : float = 4.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 16"
    fortran_name: str = "WTH(16)"
    unit        : str = "None"
    description : str = "CONS(16) The capital allocated to the investment sector should increase"


@dataclass
class WeightConstraint17:
    value       : Any
    default     : float = 4.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 17"
    fortran_name: str = "WTH(17)"
    unit        : str = "None"
    description : str = "CONS(17) As CONS(16) but when basic needs are satisfied "


@dataclass
class WeightConstraint18:
    value       : Any
    default     : float = 4.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 18"
    fortran_name: str = "WTH(18)"
    unit        : str = "None"
    description : str = "CONS(18) The GNP allocated to investment should increase"


@dataclass
class WeightConstraint19:
    value       : Any
    default     : float = 8.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 19"
    fortran_name: str = "WTH(19)"
    unit        : str = "None"
    description : str = "CONS(19) If GNP per capita exceeds 4500 U$S it should not grow more than 3% per year"


@dataclass
class WeightConstraint20:
    value       : Any
    default     : float = 6.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 20"
    fortran_name: str = "WTH(20)"
    unit        : str = "None"
    description : str = "CONS(20) Calories per capita should not exceed its upper bound"


@dataclass
class WeightConstraint21:
    value       : Any
    default     : float = 4.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 21"
    fortran_name: str = "WTH(21)"
    unit        : str = "None"
    description : str = "CONS(21) The maximum of daily calories should exceed half the the excess of calories"


@dataclass
class WeightConstraint22:
    value       : Any
    default     : float = 6.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 22"
    fortran_name: str = "WTH(22)"
    unit        : str = "None"
    description : str = "CONS(22) Daily calories should increase"


@dataclass
class WeightConstraint23:
    value       : Any
    default     : float = 8.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 23"
    fortran_name: str = "WTH(23)"
    unit        : str = "None"
    description : str = "CONS(23) Education should not grow beyond its upper bound during the optimization phase "


@dataclass
class WeightConstraint24:
    value       : Any
    default     : float = 6.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 24"
    fortran_name: str = "WTH(24)"
    unit        : str = "None"
    description : str = "CONS(24) The fraction of families with a suitable house should increase"


@dataclass
class WeightConstraint25:
    value       : Any
    default     : float = 2.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 25"
    fortran_name: str = "WTH(25)"
    unit        : str = "None"
    description : str = "CONS(25) The fraction of families with a suitable house should not be higher than 1.5 but" \
                        " if calories  or education did not reach their optimum values the upper bound is 1 "


@dataclass
class WeightConstraint26:
    value       : Any
    default     : float = 1.0
    minimum     : float = 2
    maximum     : float = 14
    name        : str = "Weight Constraint 26"
    fortran_name: str = "WTH(26)"
    unit        : str = "None"
    description : str = "CONS(26) Life expectancy should increase"
