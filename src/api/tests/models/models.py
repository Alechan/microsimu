from dataclasses import dataclass
from typing import Any

from django.db import models

from api.std_lib.lawm import variables, parameters
from api.models.fields import VariableFloatFieldMixin, ParameterIntegerFieldMixin


@dataclass
class CustomVariable(variables.ModelVariable):
    value       : Any
    name        : str = "The name"
    fortran_name: str = "The fortran name"
    unit        : str = "The unit"
    description : str = "The description"
    category    : str = "The category"


class DjangoModelWithVariableFields(models.Model):
    float_var = VariableFloatFieldMixin(model_variable=CustomVariable)


@dataclass
class CustomParameter(parameters.ModelParameter):
    value         : Any
    default_value : Any = 42
    name          : str = "The name"
    fortran_name  : str = "The fortran name"
    unit          : str = "The unit"
    description   : str = "The description"


class DjangoModelWithParameterFields(models.Model):
    integer_param = ParameterIntegerFieldMixin(model_parameter=CustomParameter)
