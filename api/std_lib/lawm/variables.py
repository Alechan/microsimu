from dataclasses import dataclass
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
