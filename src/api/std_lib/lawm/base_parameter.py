from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class ModelGeneralParameter:
    """
    A class representing parameters of a model independent of the regions. By convention, each subclass
    (like SimulationStop(ModelParameter) should:
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
class ModelRegionalParameter:
    """
    A class representing parameters of a model for the regions. By convention, each subclass
    (like SimulationStop(ModelParameter) should:
      1. Put 'value: Any' first in the list of attributes
      2. For each of the other attributes (name, fortran_name, etc) it should specify
         its type again (str) and a default value. For example, 'name : str = "Population"
      3. Even though it's not necessary for correct execution, subclassify this class to
         point the reader to this description.
     """
    value       : Any
    # "default" is  a tuple of of tuples such as dict(default) returns a {region:default} dict
    default     : tuple
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
        # Convert "default" from tuple of tuples to a {region:default} dict
        base_dict["default"] = dict(base_dict["default"])
        # Remove the value key
        del base_dict["value"]
        return base_dict
