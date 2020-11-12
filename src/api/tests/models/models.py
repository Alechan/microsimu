from dataclasses import dataclass
from typing import Any

import api.std_lib.lawm.base_parameter
from api.models.fields import *
from api.std_lib.lawm import variables


@dataclass
class CustomVariable(variables.ModelVariable):
    value       : Any
    name        : str = "The name"
    short_name  : str = "Name"
    fortran_name: str = "The fortran name"
    unit        : str = "The unit"
    description : str = "The description"
    category    : str = "The category"


class DjangoModelWithVariableFields(models.Model):
    float_var = VariableFloatField(model_variable=CustomVariable)


@dataclass
class CustomGeneralParameter(api.std_lib.lawm.base_parameter.ModelGeneralParameter):
    value         : Any
    default       : int = 5
    minimum       : int = 1
    maximum       : int = 10
    name          : str = "The name"
    fortran_name  : str = "The fortran name"
    unit          : str = "The unit"
    description   : str = "The description"


class IntegerParameterFieldDjangoModel(models.Model):
    integer_param = ParameterIntegerField(model_parameter=CustomGeneralParameter, use_parameter_default=True)


class FloatParameterFieldDjangoModel(models.Model):
    float_param = ParameterFloatField(model_parameter=CustomGeneralParameter, use_parameter_default=True)

@dataclass
class CustomRegionalParameter(api.std_lib.lawm.base_parameter.ModelGeneralParameter):
    value         : Any
    default       : dict  = (("developed", 3200), ("latinamerica", 3000), ("africa", 3000), ("asia", 3000))
    minimum       : int = 1
    maximum       : int = 10
    name          : str = "The name"
    fortran_name  : str = "The fortran name"
    unit          : str = "The unit"
    description   : str = "The description"
