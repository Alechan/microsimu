from dataclasses import dataclass
from typing import Any

from django.db import models

from api.std_lib.lawm import variables, parameters
from api.models.fields import VariableFloatField, ParameterIntegerField, ParameterFloatField


@dataclass
class CustomVariable(variables.ModelVariable):
    value       : Any
    name        : str = "The name"
    fortran_name: str = "The fortran name"
    unit        : str = "The unit"
    description : str = "The description"
    category    : str = "The category"


class DjangoModelWithVariableFields(models.Model):
    float_var = VariableFloatField(model_variable=CustomVariable)


@dataclass
class CustomParameter(parameters.ModelParameter):
    value         : Any
    default       : int = 5
    minimum       : int = 1
    maximum       : int = 10
    name          : str = "The name"
    fortran_name  : str = "The fortran name"
    unit          : str = "The unit"
    description   : str = "The description"


class IntegerParameterFieldDjangoModel(models.Model):
    integer_param = ParameterIntegerField(model_parameter=CustomParameter)


class FloatParameterFieldDjangoModel(models.Model):
    float_param = ParameterFloatField(model_parameter=CustomParameter)
